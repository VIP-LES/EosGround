from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress

from EosLib.packet.packet import Packet

import psycopg2
import time
import datetime

PORT = "COM5"
conn = psycopg2.connect(
    database="db_1", user='postgres', password='password', host='localhost', port='5432'
)
conn.autocommit = True

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

device = XBeeDevice(PORT, 9600)
device.open()

def data_receive_callback(xbee_message):
    #xbee_message.data.
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



device.add_data_received_callback(data_receive_callback)
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("13A20041CB89EE"))

while True:
    time.sleep(1)


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
