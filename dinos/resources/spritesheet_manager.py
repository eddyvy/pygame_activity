import pygame
from dinos.config import Config

from dinos.resources.asset_manager_abstract import AssetManagerAbstract
from dinos.resources.spritesheet import SpriteSheet


class SpriteSheetManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "spritesheet"))

    def _load_asset(self, asset_path, asset_name, options={}):
        data = Config.get("assets", "spritesheet", asset_name)

        image = pygame.image.load(asset_path)

        if "scale" in data:
            image = pygame.transform.scale(
                image, (image.get_width() * data["scale"], image.get_height() * data["scale"]))

        if "b_color" in data:
            image.set_colorkey(
                data["b_color"], pygame.RLEACCEL)

        image.convert_alpha

        return SpriteSheet(image, data["rows"], data["cols"])
