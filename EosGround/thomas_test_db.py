from EosLib.packet.packet import Packet
import EosLib.packet.definitions
import EosLib.packet.packet
import EosLib.packet.transmit_header
import EosLib.packet.data_header
from EosLib.device import Device
import os

import psycopg2
from config.config import get_config
from datetime import datetime

from EosLib.packet.definitions import Type

from EosLib.format.telemetry_data import TelemetryData
from EosLib.format.position import Position, FlightState
from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


global sequence_number
sequence_number = 0

conn_params = get_config(os.path.join('config', 'database.ini'))
# conn_params = get_config('/Users/aryan_battula/VIP-LES/EosGround/EosGround/config/database.ini')  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor


# function called when data is received
def data_receive_callback(xbee_message):
    try:
        cursor.execute(
            """
            INSERT INTO eos_schema.received_data (raw_bytes, rssi, processed) VALUES 
            (%s,%s,%s)
            """, (xbee_message.data, 0, False)
        )
        cursor.execute(f"NOTIFY {PacketPipeline.get_listen_channel()}")

    except psycopg2.OperationalError:
        print("Error inserting into database")

#  function called anytime new data is put into database
def send_command():
    global sequence_number
    cursor.execute("""
    SELECT * FROM eos_db.eos_schema.transmit_table WHERE time_sent is NULL
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

        #device.send_data_async(remote, packet.encode())
        sequence_number += 1
        time_sent = datetime.datetime.now()

        cursor.execute(
            """
            UPDATE eos_schema.transmit_table 
            SET time_sent = (%s)
            WHERE id = (%s)
            """, (time_sent, packet_id))


#device.add_data_received_callback(data_receive_callback)  # add data receive callback
#remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("FFFF"))  # add digi remote device

cursor.execute("LISTEN update;")  # adds listen
#while True:
#    conn.poll()
#    if len(conn.notifies) > 0:
#        print("sending command")
#        send_command()
#        conn.notifies.clear()
#    time.sleep(0.01)

class MessageWrapper:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    # POSITION
    position_data_header = EosLib.packet.data_header.DataHeader(Device.O3, Type.POSITION)
    position_transmit_header = EosLib.packet.transmit_header.TransmitHeader(2)

    current_time = datetime.now()
    new_data = Position()

    encoded_new_data = new_data.encode_position(current_time.timestamp(), 23.4, 23.4, 23.4, 23.4, 5, FlightState.NOT_SET)

    packet = Packet(encoded_new_data, position_data_header, position_transmit_header)
    wrapper = MessageWrapper(packet.encode())
    data_receive_callback(wrapper)
    # TELEMETRY
    telemetry_data_header = EosLib.packet.data_header.DataHeader(Device.MISC_1, Type.TELEMETRY_DATA)
    telemetry_transmit_header = EosLib.packet.transmit_header.TransmitHeader(3)
    telemetry = TelemetryData(
        timestamp=datetime.now(),
        temperature=3.14,
        pressure=23.32,
        humidity=234.5,
        x_rotation=0.234,
        y_rotation=0.454,
        z_rotation=2.2
    )
    telemetry_packet = Packet(
        body=telemetry.encode(),
        data_header=telemetry_data_header,
        transmit_header=telemetry_transmit_header
    )
    data_receive_callback(MessageWrapper(telemetry_packet.encode()))
