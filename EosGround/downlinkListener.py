from threading import Lock
import os

import psycopg2
import time

from config.config import get_config

conn_params = get_config(os.path.join('config', 'database.ini'))  # gets config params
conn = psycopg2.connect(**conn_params)  # gets connection object
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
cursor = conn.cursor()  # creates cursor
cursor_lock = Lock()
print("connected to database")


with cursor_lock:
    cursor.execute("LISTEN downlink;")  # adds listen
while True:
    with cursor_lock:
        conn.poll()
    if len(conn.notifies) > 0:
        print(conn.notifies)
        print('new downlink command')
        with cursor_lock:
            conn.notifies.clear()
    time.sleep(0.01)
