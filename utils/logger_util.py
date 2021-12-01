import logging
import logging.config

_log_format_default = f"%(asctime)s - [%(levelname)s] - %(name)s - " \
                      f"(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def get_logger(level: str = 'NOTSET', filename: str = None, log_format: str = _log_format_default):
    """Setting up the logger

    Args:
        level: level of logging
        filename: filename for logs
        log_format: format of logs

    """
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f'Set log level to {level}')
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': log_format,
            },
            'to_file': {
                'format': log_format,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
                'level': level.upper(),
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'to_file',
            'filename': filename if '.' in filename else filename + '.log',
            'encoding': 'utf-8',
            'maxBytes': 1024,
            'backupCount': 3,

        }

        config['root']['handlers'].append('file')

    logging.config.dictConfig(config)
