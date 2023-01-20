
from EosLib.packet.definitions import Device, Priority, Type
from config.config import config

import psycopg2
import datetime

conn_params = config('database.ini')  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor


def send_command():
    packet_generate_time = datetime.datetime.now()
    packet_sender = Device.GROUND_STATION_1
    packet_type = Type.DATA
    packet_priority = Priority.DATA
    packet_destination = Device.MISC_RADIO_1
    packet_body = "PING 422"

    cursor.execute(
        """
        INSERT INTO transmit_table (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time, packet_body) VALUES 
        (%s,%s,%s,%s,%s,%s)
        """, (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time, packet_body)
    )
    conn.commit()
    
def send_notify():
    cursor.execute("NOTIFY update;")
    conn.commit()

if __name__ == '__main__':
    send_command()
    send_notify()
    cursor.close()
    conn.close()
