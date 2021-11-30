#!/usr/bin/env python3
import argparse
import os
import sys
import logging

import server.FileService as FS
import utils.logger_util as logger_util
import utils.params_parse as params_parse
from utils.Config import Config


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -d --dir  - working directory (absolute or relative path, default: current_app_folder/data).
    -l --log_level - log level to console (default is warning)
    -f --log_file - name of log file
    -p --port - port
    -h --help - help.
    """

    params = params_parse.get_params()
    config = Config(params)
    logger_util.get_logger(level=config.data.get('log_level'), filename=config.data.get('log_file'))
    logging.info(f"Start directory: {FS.change_dir(config.data.get('dir'))}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
