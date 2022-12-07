from configparser import ConfigParser

def config(config_db):
    section = 'postgresql'
    #config_file_path = 'EosGround/EosGround/database/config/' + config_db
    config_file_path = 'config/' + config_db
    config_parser = ConfigParser()
    config_parser.read(config_file_path)
    #config_parser.read(config_db)
    config_params = config_parser.items(section)

    db_conn_dict = {}
    for config_param in config_params:
        key = config_param[0]
        value = config_param[1]
        db_conn_dict[key] = value
    return db_conn_dict