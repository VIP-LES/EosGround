import os
import psycopg2

from EosGround.config.config import get_config


def configure_db():
    print("\ncreating database...")
    conn_params = get_config(os.path.join('EosGround', 'config', 'database.ini'))
    db_name = conn_params.pop("database")
    connection = psycopg2.connect(**conn_params)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    db_script_path = os.path.join('EosGround', 'config', 'create_database.sql')
    print(f"\trunning {db_script_path}")
    with open(db_script_path) as f:
        statement = f.read().replace("placeholder_name", db_name)
        cur.execute(statement)
    connection.close()

    print("\ncreating schemas...")
    conn_params = get_config(os.path.join('EosGround', 'config', 'database.ini'))
    connection = psycopg2.connect(**conn_params)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()

    schemas = ['eos_schema', 'test_schema']
    for schema in schemas:
        schema_script_path = os.path.join('EosGround', 'config', f"{schema}.sql")
        print(f"\trunning {schema_script_path}")
        with open(schema_script_path) as f:
            cur.execute(f.read())

    print("\ndone")
    return connection


if __name__ == "__main__":
    print("WARNING: make sure working directory is the repository root")
    print("WARNING: make sure you have dropped the database in pgAdmin before running this script")
    conn = configure_db()
