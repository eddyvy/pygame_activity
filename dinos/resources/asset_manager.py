from importlib import resources
from os import path

import pygame

from dinos.resources.font_manager import FontManager
from dinos.resources.music_manager import MusicManager
from dinos.resources.sfx_manager import SfxManager


class AssetManager:

    __instance = None

    @staticmethod
    def instance():
        if AssetManager.__instance is None:
            AssetManager()
        return AssetManager.__instance

    def __init__(self):
        if not AssetManager.__instance is None:
            raise Exception("There Can Be Only One AssetManager!!!")
        AssetManager.__instance = self

        self.font = FontManager()
        self.music = MusicManager()
        self.sfx = SfxManager()

    def clean(self, state):
        self.font.clean(state)
        self.music.clean(state)
        self.sfx.clean(state)
