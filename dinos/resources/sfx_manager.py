import pygame

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class SfxManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "sfx"))

    def _load_asset(self, asset_path, options={}):
        return pygame.mixer.Sound(asset_path)
