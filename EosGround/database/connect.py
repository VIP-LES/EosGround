from sqlalchemy import Connection, Engine, create_engine

import EosGround.config.config as Config


def connect(config_filepath: str = 'database.ini', autoconnect: bool = True,
            verbose: bool = False) -> Connection | Engine:
    config = Config.get_config(config_filepath, dbsection="host-postgresql")
    connect_string = f"postgresql+psycopg2://{config['user']}:{config['password']}"\
                     f"@{config['host']}:{config['port']}/{config['database']}"
    engine = create_engine(connect_string, echo=verbose)
    return engine.connect() if autoconnect else engine

def connect_docker(config_filepath: str = 'database.ini', autoconnect: bool = True,
            verbose: bool = False) -> Connection | Engine:
    config = Config.get_config(config_filepath)
    connect_string = f"postgresql+psycopg2://postgres:password"\
                     f"@postgres:5432/eos_db"
    engine = create_engine(connect_string, echo=verbose)
    return engine.connect() if autoconnect else engine

