import json
from importlib import resources

import pygame


class Config:

    __config_files_path = "dinos.assets.config"
    __instance = None

    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if not Config.__instance is None:
            raise Exception("There Can Be Only One Config!!!")

        Config.__instance = self

        self.data = {}
        json_files_names = [f for f in resources.contents(
            Config.__config_files_path) if f.endswith(".json")]
        for json_file_name in json_files_names:
            with resources.path(Config.__config_files_path, json_file_name) as json_file:
                name = json_file_name.split(".json")[0]
                with open(json_file) as file:
                    self.data[name] = json.load(file)

    @staticmethod
    def get(*items):
        data = Config.instance().data
        for key in items:
            data = data[key]
        return data
