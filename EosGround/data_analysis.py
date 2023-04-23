
import os
import psycopg2

from EosLib.packet.packet import Packet
from EosLib.packet.definitions import Type
from EosLib.format.telemetry_data import TelemetryData


from config.config import get_config

conn_params = get_config(os.path.join('config', 'database.ini'))  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor
print("connected to database")

cursor.execute("""
    SELECT * FROM eos_schema.received_data
    ORDER BY "id" ASC 
    """)

rows = cursor.fetchall()

for i in range(1):
    first_row = rows[0]
    id = first_row[0]
    packet_bytes = bytes(first_row[1])
    packet = Packet.decode(packet_bytes)

    send_time = packet.transmit_header.send_time
    seq_num = packet.transmit_header.send_seq_num
    data_type = packet.data_header.data_type
    sender = packet.data_header.sender
    destination = packet.data_header.destination
    body = packet.body

    print(data_type)
    print(body)

    if data_type == Type.TELEMETRY_DATA:
        packet_data = TelemetryData.decode_data(body)
        print("TELEMETRY_DATA")



#packet_obj = Packet.encode(packet_bytes)

#print(packet)