import pygame

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class ImageManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "image"))

    def _load_asset(self, asset_path, asset_name, options={}):
        return pygame.image.load(asset_path).convert_alpha()
