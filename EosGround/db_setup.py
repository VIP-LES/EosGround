import psycopg2
from config.config import config

conn_params = config('database.ini')
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
        packet_body VARCHAR(255) NOT NULL,
        time_arrived timestamp NOT NULL
        )
        """
    )
except:
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
except:
    print("TX table exists")