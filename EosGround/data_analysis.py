
import os
import psycopg2
import csv

from EosLib.packet.packet import Packet
from EosLib.packet.definitions import Type
from EosLib.format.telemetry_data import TelemetryData
from EosLib.format.position import Position

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

tel_counter = 0
pos_counter = 0
other_counter = 0

f_tel = open('FlightData/telemetry.csv', 'w', newline='')
f_pos = open('FlightData/position.csv', 'w', newline='')
f_other = open('FlightData/other.csv', 'w', newline='')

writer_tel = csv.writer(f_tel)
writer_pos = csv.writer(f_pos)
writer_other = csv.writer(f_other)

for i in range(len(rows)):
    row = rows[i]
    id = row[0]
    packet_bytes = bytes(row[1])
    packet = Packet.decode(packet_bytes)

    send_time = packet.transmit_header.send_time
    seq_num = packet.transmit_header.send_seq_num
    data_type = packet.data_header.data_type
    sender = packet.data_header.sender
    destination = packet.data_header.destination
    body = packet.body

    if data_type == Type.TELEMETRY_DATA:
        packet_data = TelemetryData.decode_data(body)
        temperature = packet_data.temperature
        pressure = packet_data.pressure
        humidity = packet_data.humidity
        x_rotation = packet_data.x_rotation
        y_rotation = packet_data.y_rotation
        z_rotation = packet_data.z_rotation
        tel_row = [id, send_time, temperature, pressure, humidity, x_rotation, y_rotation, z_rotation]
        writer_tel.writerow(tel_row)
        tel_counter += 1

    elif data_type == Type.POSITION:
        packet_data = Position.decode_position(body)
        latitude = packet_data.latitude
        longitude = packet_data.longitude
        altitude = packet_data.altitude
        speed = packet_data.speed
        number_of_satellites = packet_data.number_of_satellites
        flight_state = packet_data.flight_state
        pos_row = [id, send_time, latitude, longitude, altitude, speed, number_of_satellites, flight_state]
        writer_pos.writerow(pos_row)
        pos_counter += 1

    elif data_type == Type.TELEMETRY:
        other_counter += 1
        other_row = [id, send_time, body.decode()]
        writer_other.writerow(other_row)

print(tel_counter)
print(pos_counter)
print(other_counter)

f_tel.close()
f_pos.close()
f_other.close()
