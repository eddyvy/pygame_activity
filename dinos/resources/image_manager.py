import pygame
from dinos.config import Config

from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class ImageManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "image"))

    def _load_asset(self, asset_path, asset_name, options={}):
        data = Config.get("assets", "image", asset_name)
        image = pygame.image.load(asset_path)

        if "size" in data:
            image = pygame.transform.scale(image, (
                data["size"][0],
                data["size"][1]
            ))

        return image.convert_alpha()
