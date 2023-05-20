from enum import Enum
from importlib import resources
from os import path

import pygame
from dinos.config import Config

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class SfxManager(AssetManagerAbstract):

    __CONFIG_FILE = "assets", "sfx"

    def __init__(self):
        super().__init__()

    def load(self, state, asset_name, options={}):
        if not state in self._assets:
            self._assets[state] = {}

        with resources.path(*Config.get(*self.__CONFIG_FILE, asset_name, "file")) as asset_path:
            if path.isfile(asset_path) and asset_name not in self._assets[state]:
                self._assets[state][asset_name] = pygame.mixer.Sound(
                    asset_path)
