import os
import psycopg2

from config.config import get_config

conn_params = get_config(os.path.join('config', 'database.ini'))
connection = psycopg2.connect(**conn_params)
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = connection.cursor()

try:
    cur.execute(
        """
        CREATE TABLE receive_table (
        id SERIAL PRIMARY KEY,
        packet_type INT NOT NULL,
        packet_sender INT NOT NULL,
        packet_priority INT NOT NULL,
        packet_generate_time timestamp NOT NULL,
        packet_sequence_number INT NOT NULL,
        packet_timestamp timestamp NOT NULL,
        packet_body bytea NOT NULL,
        packet_destination INT,
        time_arrived timestamp NOT NULL
        )
        """
    )
except psycopg2.errors.DuplicateTable:
    print("RX table exists")

try:
    cur.execute(
        """
        CREATE TABLE transmit_table (
        id SERIAL PRIMARY KEY,
        time_sent timestamp default NULL,
        packet_type INT NOT NULL,
        packet_sender INT NOT NULL,
        packet_priority INT NOT NULL,
        packet_destination INT NOT NULL,
        packet_generate_time timestamp NOT NULL,
        packet_body VARCHAR(255) NOT NULL
        )
        """
    )
except psycopg2.errors.DuplicateTable:
    print("TX table exists")
