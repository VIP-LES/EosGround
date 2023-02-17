import psycopg2
from config.config import config


def configure_db():
    conn_params = config('database.ini')
    connection = psycopg2.connect(**conn_params)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    with open("config/eos_schema.sql") as f:
        cur.execute(f.read())
    return connection


if __name__ == "__main__":
    conn = configure_db()
