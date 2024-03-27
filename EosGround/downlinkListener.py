from threading import Lock
import os
from datetime import datetime

import psycopg2
import time

from EosLib.packet.definitions import Priority
from EosLib.format.definitions import Type
from EosGround.downlink_receiver import DownlinkReceiver
from EosLib.format.formats.downlink_header_format import DownlinkCommandFormat, DownlinkCommand
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

from EosLib.device import Device

from config.config import get_config

conn_params = get_config(os.path.join('config', 'database.ini'))  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor
cursor_lock = Lock()
print("connected to database")


last_check_time = datetime.now()

while True:
    with cursor_lock:
        conn.poll()

    print("checking for any downlink acks from payload...")
    cursor.execute("""
        SELECT eos_schema.downlink_command.file_id, eos_schema.downlink_command.num_chunks, eos_schema.downlink_command.command_type
        FROM eos_schema.downlink_command
        JOIN eos_schema.received_packets ON eos_schema.downlink_command.packet_id = eos_schema.received_packets.id
        WHERE eos_schema.received_packets.received_time > %s;
    """, (last_check_time,))
    downlink_commands = cursor.fetchall()
    last_check_time = datetime.now()

    if downlink_commands:
        print("received downlink ack from payload, creating receiver")
        downlink_command = downlink_commands[-1]
        file_id, num_chunks, command_type = downlink_command
        downlink_header = DownlinkCommandFormat(file_id, num_chunks, command_type)
        receiver = DownlinkReceiver(downlink_header)

        packet_generate_time = datetime.datetime.now()
        packet_sender = Device.GROUND_STATION_1
        packet_type = Type.DOWNLINK_COMMAND
        packet_priority = Priority.DATA
        packet_destination = Device.DOWNLINK
        packet_body = DownlinkCommandFormat(file_id, num_chunks, DownlinkCommand.START_ACK)

        # converted packet_body to binary
        packet_body_bytes = packet_body.encode()

        print("sending downlink ack back to payload")
        cursor.execute(
            """
            INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time, packet_body_bytes)
        )
        conn.commit()
        print("downlink command ack sent")

        last_chunk_time = datetime.now()

        chunks_query = """
                    SELECT eos_schema.downlink_chunk.chunk_num, eos_schema.downlink_chunk.chunk_body
                    FROM eos_schema.downlink_chunk
                    JOIN received_packets ON downlink_chunk.packet_id = received_packets.id
                    WHERE received_packets.received_time > %s;
                """
        while True:
            print("checking for any new chunks")
            cursor.execute(chunks_query, (last_chunk_time,))
            chunks = cursor.fetchall()
            if chunks:
                print("found new chunks, waiting for all chunks to arrive")
                time.sleep(10)
                cursor.execute(chunks_query, (last_chunk_time,))
                chunks = cursor.fetchall()
                last_chunk_time = datetime.now()
                print("writing chunks to receiver")
                for chunk in chunks:
                    downlink_chunk = DownlinkChunkFormat(chunk_num=chunk[0], chunk_body=chunk[1])
                    receiver.write_chunk(downlink_chunk)
                ack_packet = receiver.get_ack()

                print("checking for missing chunks")
                if ack_packet.missing_chunks:
                    print(f"Missing chunks: {ack_packet.missing_chunks}")
                    packet_generate_time = datetime.datetime.now()
                    packet_sender = Device.GROUND_STATION_1
                    packet_type = Type.DOWNLINK_COMMAND
                    packet_priority = Priority.DATA
                    packet_destination = Device.DOWNLINK
                    packet_body = DownlinkCommandFormat(file_id, num_chunks, DownlinkCommand.RETRANSMIT_MISSING_CHUNKS, ack_packet.missing_chunks)

                    # converted packet_body to binary
                    packet_body_bytes = packet_body.encode()

                    cursor.execute(
                        """
                        INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """,
                        (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time,
                         packet_body_bytes)
                    )
                    conn.commit()
                    print("missing chunks sent back to payload")
                else:
                    print("no missing chunks detected, stopping transmission")
                    packet_generate_time = datetime.datetime.now()
                    packet_sender = Device.GROUND_STATION_1
                    packet_type = Type.DOWNLINK_COMMAND
                    packet_priority = Priority.DATA
                    packet_destination = Device.DOWNLINK
                    packet_body = DownlinkCommandFormat(file_id, num_chunks, DownlinkCommand.STOP_TRANSMISSION,
                                                        ack_packet.missing_chunks)

                    # converted packet_body to binary
                    packet_body_bytes = packet_body.encode()

                    cursor.execute(
                        """
                        INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """,
                        (packet_type, packet_sender, packet_priority, packet_destination, packet_generate_time,
                         packet_body_bytes)
                    )
                    conn.commit()
                    print("sent stop transmission downlink command to payload")

            time.sleep(10)
    time.sleep(10)
