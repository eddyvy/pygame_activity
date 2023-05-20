from abc import ABC, abstractmethod
from importlib import resources
from os import path

import pygame


class AssetManagerAbstract(ABC):

    def __init__(self):
        self._assets = {}

    @abstractmethod
    def load(self, asset_name, options={}):
        pass

    def get(self, state, asset_name):
        return self._assets[state][asset_name]

    def clean(self, state):
        if state in self._assets:
            del self._assets[state]
