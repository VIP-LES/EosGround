from configparser import ConfigParser


def get_config(config_file_path: str) -> dict:
    section = 'postgresql'
    config_parser = ConfigParser()
    config_parser.read(config_file_path)
    config_params = config_parser.items(section)

    db_conn_dict = {}
    for config_param in config_params:
        key = config_param[0]
        value = config_param[1]
        db_conn_dict[key] = value
    return db_conn_dict
