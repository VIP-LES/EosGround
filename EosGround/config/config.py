from configparser import ConfigParser, NoSectionError


def get_config(config_file_path: str) -> dict:
    section = 'postgresql'
    config_parser = ConfigParser()
    config_parser.read(config_file_path)
    try:
        print("config_file_path: " + config_file_path)
        config_params = config_parser.items(section)
    except NoSectionError as err:
        print(f"*** ERROR: either the `config_file_path` is not correct or the config file doesn't have a"
              f" '{section}' section ***"
              f"\nprovided `config_file_path`: {config_file_path}")
        raise err

    db_conn_dict = {}
    for config_param in config_params:
        key = config_param[0]
        value = config_param[1]
        db_conn_dict[key] = value
    return db_conn_dict
