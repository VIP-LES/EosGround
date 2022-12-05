
from EosLib.packet.packet import Packet
import EosLib.packet.definitions as PacketDefinitions

import psycopg2
import datetime

conn = psycopg2.connect(
    database="db_1", user='postgres', password='password', host='localhost', port='5432'
)

# Creating a cursor object using the cursor() method
cursor = conn.cursor()


def send_command():
    time_sent = datetime.datetime.now()
    packet_generate_time = datetime.datetime.now()
    packet_sender = PacketDefinitions.Device.GROUND_STATION_1
    packet_type = PacketDefinitions.Type.DATA
    packet_priority = PacketDefinitions.Priority.DATA
    packet_destination = PacketDefinitions.Device.RADIO
    packet_body = "Data"

    cursor.execute(
        """
        INSERT INTO transmit_table (time_sent, packet_type, packet_sender, packet_priority, packet_generate_time, packet_body) VALUES 
        (%s,%s,%s,%s,%s,%s)
        """, (time_sent, packet_type, packet_sender, packet_priority, packet_generate_time, packet_body)
    )
    conn.commit()
    
def send_notify():
    cursor.execute("NOTIFY update;")
    conn.commit()

if __name__ == '__main__':
    #send_command()
    send_notify()
    cursor.close()
    conn.close()