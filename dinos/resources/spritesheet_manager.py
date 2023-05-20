import pygame
from dinos.config import Config

from dinos.resources.asset_manager_abstract import AssetManagerAbstract
from dinos.resources.spritesheet import SpriteSheet


class SpriteSheetManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "spritesheet"))

    def _load_asset(self, asset_path, asset_name, options={}):
        rows = Config.get("assets", "spritesheet", asset_name, "rows")
        cols = Config.get("assets", "spritesheet", asset_name, "cols")
        image = pygame.image.load(asset_path).convert_alpha()
        scale = Config.get("assets", "spritesheet", asset_name, "scale")
        image = pygame.transform.scale(
            image, (image.get_width() * scale, image.get_height() * scale))
        return SpriteSheet(image, rows, cols)
