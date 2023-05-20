from abc import ABC, abstractmethod
from importlib import resources
from os import path

from dinos.config import Config


class AssetManagerAbstract(ABC):

    def __init__(self, config_file):
        self.__assets = {}
        self.__assets_states_using = {}
        self.__config_file = config_file

    @abstractmethod
    def _load_asset(self, asset_path, asset_name, options={}):
        pass

    def load(self, state, asset_name, options={}):
        if asset_name not in self.__assets_states_using:
            self.__assets_states_using[asset_name] = {}

        self.__assets_states_using[asset_name][state] = True

        with resources.path(*Config.get(*self.__config_file, asset_name, "file")) as asset_path:
            if path.isfile(asset_path) and asset_name not in self.__assets:
                self.__assets[asset_name] = self._load_asset(
                    asset_path, asset_name, options)

    def get(self, asset_name):
        return self.__assets[asset_name]

    def clean(self, state=None):
        if state == None:
            self.__assets = {}
            self.__assets_states_using = {}
            return

        for a_name in list(self.__assets_states_using.keys()):
            if self.__assets_states_using[a_name][state]:
                del self.__assets_states_using[a_name][state]
            if not self.__assets_states_using[a_name]:
                del self.__assets_states_using[a_name]
                del self.__assets[a_name]
