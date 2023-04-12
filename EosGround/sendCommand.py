
from EosLib.packet.definitions import Priority, Type
from EosLib.device import Device
from config.config import get_config
import os

import psycopg2
import datetime

conn_params = get_config(os.path.join('config', 'database.ini'))  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor


def send_command():
    packet_generate_time = datetime.datetime.now()
    packet_sender = Device.GROUND_STATION_1
    packet_type = Type.DATA
    packet_priority = Priority.DATA
    packet_destination = Device.MISC_ENGINEERING_2
    packet_body = "PING 422"

    cursor.execute(
        """
        INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body) VALUES 
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
