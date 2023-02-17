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
PORT = "COM12"
device = XBeeDevice(PORT, 9600)
device.open()


# function called when data is received
def data_receive_callback(xbee_message):
    try:
        cursor.execute(
            """
            INSERT INTO received_data (raw_bytes, rssi, processed) VALUES 
            (%s,%s,%s)
            """, (xbee_message.data, device.get_parameter("DB"), False)
        )
    except psycopg2.OperationalError:
        print("Error inserting into database")


#  function called anytime new data is put into database
def send_command():
    global sequence_number
    cursor.execute("""
    SELECT * FROM "transmit_table" WHERE time_sent is NULL
    ORDER BY "id" DESC
    """)

    cmdrows = cursor.fetchall()

    for row in cmdrows:
        packet_id = row[0]
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
        time_sent = datetime.datetime.now()

        cursor.execute(
            """
            UPDATE transmit_table 
            SET time_sent = (%s)
            WHERE id = (%s)
            """, (time_sent, packet_id))


device.add_data_received_callback(data_receive_callback)  # add data receive callback
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("FFFF"))  # add digi remote device

cursor.execute("LISTEN update;")  # adds listen
while True:
    conn.poll()
    if len(conn.notifies) > 0:
        print("sending command")
        send_command()
        conn.notifies.clear()
    time.sleep(0.01)
