import sys

from EosLib.packet.definitions import Priority
from EosLib.format.definitions import Type

from config.config import get_config
from EosLib.device import Device

import psycopg2
import datetime

import os

conn_params = get_config(os.path.join('config', 'database.ini'))
# conn_params = get_config(os.path.join('EosGround', 'config', 'database.ini'))  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor


def send_ping_command():
    packet_generate_time = datetime.datetime.now()
    packet_sender = Device.GROUND_STATION_1
    packet_type = Type.DATA
    packet_priority = Priority.DATA
    packet_destination = Device.MISC_RADIO_1
    packet_body = "PING 422"

    #converted packet_body to binary
    packet_body_bytes = packet_body.encode()

    cursor.execute(
        """
        INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time, packet_body_bytes)
    )
    conn.commit()
    print("Ping command sent")


def send_cutdown_command():
    ans = input("Are you sure you want to trigger the cutdown?  (y/n):\t")
    if ans.lower() == 'y':
        packet_generate_time = datetime.datetime.now()
        packet_sender = Device.GROUND_STATION_1
        packet_type = Type.DATA
        packet_priority = Priority.DATA
        packet_destination = Device.CUTDOWN
        packet_body = "DEWIT!"

        packet_body_bytes = packet_body.encode()

        cursor.execute(
            """
            INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
            VALUES (%s,%s,%s,%s,%s,%s)
            """, (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time, packet_body_bytes)
        )
        conn.commit()
        print("Cutdown command sent")


def send_notify():
    cursor.execute("NOTIFY update;")
    conn.commit()
    print("NOTIFY issued")


if __name__ == '__main__':
    # ping: python EosGround/sendCommand.py ping
    # cutdown: python EosGround/sendCommand.py cutdown
    if sys.argv[1] == "ping":
        send_ping_command()
    elif sys.argv[1] == "cutdown":
        send_cutdown_command()
    else:
        print("Invalid command")
    send_notify()
    cursor.close()
    conn.close()
