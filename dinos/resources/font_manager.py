import pygame

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class FontManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "fonts"))

    def _load_asset(self, asset_path, options={}):
        return pygame.font.Font(asset_path, options["font_size"])
