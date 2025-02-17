# activate the virtual environment
# source venv/bin/activate
# run the script with PYTHONPATH="/Users/regmi/Desktop/EosGround" python3 EosGround/radioDriver.py
from threading import Lock
import datetime
import os
import traceback

import psycopg2
import time

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
from digi.xbee.devices import TransmitOptions

from EosLib.packet.packet import Packet
import EosLib.packet.definitions
import EosLib.packet.packet
import EosLib.packet.transmit_header
from EosLib.format.definitions import Type

from EosLib.format.formats.cutdown import CutDown
from EosLib.format.decode_factory import decode_factory

from EosGround.config.config import get_config
from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline

global sequence_number
sequence_number = 0

conn_params = get_config(os.path.join('EosGround/config', 'database.ini'), dbsection="host-postgresql")  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor
cursor_lock = Lock()
print("connected to database")

# sets up digi

# Batshal's port
PORT = "/dev/cu.usbserial-FT5PFML62"
# aryan's port:
# PORT = "/dev/cu.usbserial-FT5PG7VE2"
#panya's port:
# PORT = "/dev/cu.usbserial-FT5PFML62"
device = XBeeDevice(PORT, 9600)
device.open()
print("connected to xbee")


# function called when data is received
def data_receive_callback(xbee_message):
    try:
        with cursor_lock:
            received_time = datetime.datetime.now()
            # places xbee_message into received_data table
            cursor.execute(
                """
                INSERT INTO eos_schema.received_data (raw_bytes, rssi, processed, received_time) VALUES 
                (%s,%s,%s,%s)
                """, (xbee_message.data, 0, False, received_time)
            )
            # creates notify message to start pipeline
            cursor.execute(f"NOTIFY {PacketPipeline.get_listen_channel()}")

    except psycopg2.OperationalError:
        print("Error inserting into database")


#  function called anytime new data is put into database
def send_command():
    global sequence_number
    with cursor_lock:
        cursor.execute("""
        SELECT * FROM eos_schema.transmit_table WHERE time_sent is NULL
        ORDER BY "id" DESC
        """)

        cmdrows = cursor.fetchall()

    print(f"Sending {len(cmdrows)} commands")

    for row in cmdrows:
        try:
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

            packet_body = decode_factory.decode(packet_type, packet_body.tobytes())

            transmit_header = EosLib.packet.transmit_header.TransmitHeader(sequence_number)
            transmit_header.send_time = datetime.datetime.now()

            packet = Packet(data_header=data_header, body=packet_body)  # transmit packet
            packet.transmit_header = transmit_header

            device.send_data_async(remote, packet.encode(), transmit_options=TransmitOptions.DISABLE_ACK.value)
            sequence_number += 1
            with cursor_lock:
                time_sent = datetime.datetime.now()

                cursor.execute(
                    """
                    UPDATE eos_schema.transmit_table 
                    SET time_sent = (%s)
                    WHERE id = (%s)
                    """, (time_sent, packet_id))
        except Exception as e:
            print(f"Failed to send command: {e}\n{traceback.print_exc()}")


device.add_data_received_callback(data_receive_callback)  # add data receive callback
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("000000000000FFFF"))  # add digi remote device

with cursor_lock:
    cursor.execute("LISTEN update;")  # adds listen
while True:
    with cursor_lock:
        conn.poll()
    if len(conn.notifies) > 0:
        print('transmitted')
        send_command()
        with cursor_lock:
            conn.notifies.clear()
    time.sleep(0.01)
