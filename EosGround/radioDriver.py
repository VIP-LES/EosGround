import time

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress

from EosLib.packet.packet import Packet
import EosLib.packet.definitions
import EosLib.packet.packet
import EosLib.packet.transmit_header

import psycopg2
from config.config import config
import datetime

global sequence_number
sequence_number = 0

conn_params = config('database.ini')  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor

# sets up digi
PORT = "COM5"
device = XBeeDevice(PORT, 9600)
device.open()


# function called when data is received
def data_receive_callback(xbee_message):
    packet = Packet.decode(xbee_message.data)

    packet_type = packet.data_header.data_type
    packet_sender = packet.data_header.sender
    packet_priority = packet.data_header.priority
    packet_generate_time = packet.data_header.generate_time
    packet_sequence_number = packet.transmit_header.send_seq_num
    packet_timestamp = packet.transmit_header.send_time
    packet_body = packet.body.decode()
    time_arrived = datetime.datetime.now()

    print(packet_body)

    cursor.execute(
        """
        INSERT INTO receive_table (packet_type, packet_sender, packet_priority, packet_generate_time, packet_sequence_number, packet_timestamp, packet_body, time_arrived) VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
        packet_type, packet_sender, packet_priority, packet_generate_time, packet_sequence_number, packet_timestamp,
        packet_body, time_arrived)
    )
    conn.commit()


#  function called anytime new data is put into database
def send_command():
    global sequence_number
    cursor.execute("""
    SELECT * FROM "transmit_table"
    ORDER BY "id" DESC
    LIMIT 1;
    """)

    row = cursor.fetchall()[0] # gets last row in table
    print(row)
    packet_type = row[2]
    packet_sender = row[3]
    packet_priority = row[4]
    packet_destination = row[5]
    packet_generate_time = row[6]
    packet_body = row[7]

    sequence_number = (sequence_number + 1) % 256

    data_header = EosLib.packet.packet.DataHeader(sender=packet_sender)  # create data header
    data_header.data_type = packet_type
    data_header.priority = packet_priority
    data_header.generate_time = packet_generate_time

    data_header.destination = packet_destination  # added externally

    transmit_header = EosLib.packet.transmit_header.TransmitHeader(sequence_number)
    transmit_header.send_time = datetime.datetime.now()

    packet = Packet(data_header=data_header, body=packet_body.encode())  # transmit packet
    packet.transmit_header = transmit_header

    device.send_data_async(remote, packet.encode())
    sequence_number += 1


device.add_data_received_callback(data_receive_callback)  # add data receive callback
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("FFFF"))  # add digi remote device

cursor.execute("LISTEN update;")  # adds listen
while True:
    conn.poll()
    for notify in conn.notifies:
        print("sending command")
        send_command()
        conn.notifies.clear()
    time.sleep(0.01)
