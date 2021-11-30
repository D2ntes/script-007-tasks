import os
import configparser
from utils.singleton import singleton

DEFAULT_CONFIG = "config.ini"
APP_NAME = "FILE_SERVER"


@singleton
class Config:
    def __init__(self, start_params: dict = None):
        self.data = start_params
        self.update_data()

    def update_data(self):
        self.read_ini()
        self.read_env()

    def read_env(self):
        for param in self.data:
            if os.environ.get(param, None):
                self[param] = os.environ[f"{APP_NAME}_{param.upper()}"]

    def read_ini(self):
        parser = configparser.ConfigParser()
        parser.read(DEFAULT_CONFIG)

        for section in parser.sections():
            for key, value in parser[section].items():
                if not self.data.get(key):
                    self.data[key] = value
