import argparse
import os

params_keys = ['dir', 'log_level', 'log_file',  'port']


def get_params():
    start_params = dict()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='data', type=str,
                        help="working directory (default: 'data')")
    parser.add_argument('-l', '--log_level', default='warning', choices=['debug', 'info', 'warning', 'error'],
                        help='log level to console (default is warning)')
    parser.add_argument('-f', '--log_file', type=str, help='name of log file')
    parser.add_argument('-p', '--port', type=int, help='port', default=8080)
    params = parser.parse_args()

    for key in params_keys:
        value = getattr(params, key, None)

        if value:
            if key == 'dir':
                start_params[key] = value if os.path.isabs(value) else os.path.join(os.getcwd(), value)
            else:
                start_params[key] = value

    return start_params
