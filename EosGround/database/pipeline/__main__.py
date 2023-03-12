from argparse import ArgumentParser
import os

from EosGround.database.pipeline.lib.runner import Runner


if __name__ == '__main__':
    # read args
    parser = ArgumentParser()
    default_config_filepath = os.path.join('.', 'EosGround', 'config', 'database.ini')
    parser.add_argument('-c', '--config-filepath', required=False, default=default_config_filepath)
    parser.add_argument('-d', '--debug', required=False, action='store_true', default=False)

    args = parser.parse_args()

    # do the things
    runner = Runner(args.config_filepath, args.debug)
    runner.run()
