import os
import psycopg2

from config.config import get_config


def configure_db():
    conn_params = get_config(os.path.join('config', 'database.ini'))
    db_name = conn_params.pop("database")
    connection = psycopg2.connect(**conn_params)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    with open("config/create_database.sql") as f:
        statement = f.read().replace("placeholder_name", db_name)
        cur.execute(statement)
    connection.close()

    conn_params = get_config(os.path.join('config', 'database.ini'))
    connection = psycopg2.connect(**conn_params)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    with open("config/eos_schema.sql") as f:
        cur.execute(f.read())
    return connection


if __name__ == "__main__":
    conn = configure_db()
