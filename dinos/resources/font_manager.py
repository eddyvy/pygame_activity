from importlib import resources
from os import path

import pygame

from dinos.config import Config


class FontManager:

    __instance = None

    @staticmethod
    def instance():
        if FontManager.__instance is None:
            FontManager()
        return FontManager.__instance

    def __init__(self):
        if not FontManager.__instance is None:
            raise Exception("There Can Be Only One FontManager!!!")

        FontManager.__instance = self
        self.__fonts = {}

    def load(self, state, font_name, font_filepath, font_size):
        if not state in self.__fonts:
            self.__fonts[state] = {}

        with resources.path(font_filepath[0], font_filepath[1]) as font_path:
            if path.isfile(font_path) and font_name not in self.__fonts[state]:
                self.__fonts[state][font_name] = pygame.font.Font(
                    font_path,
                    font_size
                )

    def get(self, state, font_name):
        return self.__fonts[state][font_name]

    def clean(self, state):
        del self.__fonts[state]
