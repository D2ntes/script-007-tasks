#!/usr/bin/env python3
import sys
import logging
from aiohttp import web

import utils.logger_util as logger_util
import utils.params_parse as params_parse
from utils.Config import Config
from server.WebHandler import WebHandler


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

    handler = WebHandler(config.data.get('dir'))
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/create_file', handler.create_file),
        web.post('/change_dir', handler.change_dir),
        web.get('/get_files', handler.get_files),
        web.get('/get_file_data', handler.get_file_data),
        web.delete('/delete_file', handler.delete_file),
    ])

    logging.info(f"Starting server on {config.data.get('host')}, port {config.data.get('port')}")
    web.run_app(app, host=config.data.get('host'), port=config.data.get('port'))



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
