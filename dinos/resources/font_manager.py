import pygame
from dinos.config import Config

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class FontManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "fonts"))

    def _load_asset(self, asset_path, asset_name, options={}):
        font_size = options["font_size"] if "font_size" in options else Config.get(
            "assets", "fonts", asset_name, "font_size")
        return pygame.font.Font(asset_path, font_size)
