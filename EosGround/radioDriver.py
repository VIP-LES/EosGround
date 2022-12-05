import time

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress

from EosLib.packet.packet import Packet
import EosLib.packet.definitions
import EosLib.packet.packet
import EosLib.packet.transmit_header

import psycopg2
import datetime

PORT = "COM5"
conn = psycopg2.connect(
    database="db_1", user='postgres', password='password', host='localhost', port='5432'
)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

device = XBeeDevice(PORT, 9600)
device.open()

def data_receive_callback(xbee_message):
    packet = Packet.decode(xbee_message.data)

    packet_type = packet.data_header.data_type
    packet_sender = packet.data_header.sender
    packet_priority = packet.data_header.priority
    packet_generate_time = packet.data_header.generate_time
    packet_sequence_number = packet.transmit_header.send_seq_num
    packet_timestamp = packet.transmit_header.send_time
    packet_body = packet.body.decode()
    #time_arrived = xbee_message.timestamp
    time_arrived = datetime.datetime.now()

    print(packet_body)

    cursor.execute(
        """
        INSERT INTO receive_table (packet_type, packet_sender, packet_priority, packet_generate_time, packet_sequence_number, packet_timestamp, packet_body, time_arrived) VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (packet_type, packet_sender, packet_priority, packet_generate_time, packet_sequence_number, packet_timestamp, packet_body, time_arrived)
    )
    conn.commit()

def send_command():
    cursor.execute( """
    SELECT * FROM "transmit_table"
    ORDER BY "id" DESC
    LIMIT 1;
    """)

    row = cursor.fetchall()[0]
    print(row)
    packet_type = row[2]
    packet_sender = row[3]
    packet_priority = row[4]
    packet_generate_time = row[5]
    packet_body = row[6]
    packet_sequence_number = 100

    data_header = EosLib.packet.packet.DataHeader(sender=packet_sender)
    data_header.data_type = packet_type
    data_header.priority = packet_priority
    data_header.generate_time = packet_generate_time
    data_header.destination = EosLib.packet.definitions.Device.RADIO

    transmit_header = EosLib.packet.transmit_header.TransmitHeader(packet_sequence_number)
    transmit_header.send_time = datetime.datetime.now()

    packet = Packet(data_header=data_header, body=packet_body.encode())
    packet.transmit_header = transmit_header

    device.send_data_async(remote, packet.encode())

device.add_data_received_callback(data_receive_callback)
#remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("13A20041CB89EE"))
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("FFFF"))

cursor.execute("LISTEN update;")
while True:
    conn.poll()
    for notify in conn.notifies:
        print("sending command")
        send_command()
        conn.notifies.clear()
    time.sleep(0.01)

'''
# Creating a database
#cursor.execute("CREATE TABLE data(id SERIAL_PRIMARY_KEY ,name Raw, name Read)")
#conn.commit()
#print("Database created successfully........")

# Closing the connection
conn.close()
class RadioDriver():
    device = XBeeDevice("COM9", 9600)
    device.open()

    # Closing the connection
    conn.close()
    def radio_read(self):
        ##read from digi
        message = self.device.add_data_received_callback(self.data_receive_callback)
        ##write to database
        cursor.execute("INSERT INTO data (id) VALUE(%s)",SERIAL_PRIMARY_KEY)

        ##PRIMARY_KEY AUTO_INCREMENT;
        return 0
    def radio_send(self):
        ##read from database
        ##send to database
        return 0
    def data_receive_callback(xbee_message):
        packet = xbee_message.data.decode()
        return packet
        ##self.logger.info("Packet received ~~~~~~")
        ##self.logger.info(packet)

    ##CREATE TABLE data(
      ##  id  SERIAL PRIMARY KEY;
   ## );

'''
'''
def send_command():
    time_sent = datetime.datetime.now()
    packet_generate_time = datetime.datetime.now()
    packet_sender = PacketDefinitions.Device.GROUND_STATION_1
    packet_type = PacketDefinitions.Type.DATA
    packet_priority = PacketDefinitions.Priority.DATA
    packet_body = "Data"

    cursor.execute(
        """
        INSERT INTO transmit_table (time_sent, packet_type, packet_sender, packet_priority, packet_generate_time, packet_body) VALUES 
        (%s,%s,%s,%s,%s,%s)
        """, (time_sent, packet_type, packet_sender, packet_priority, packet_generate_time, packet_body)
    )
    conn.commit()
'''