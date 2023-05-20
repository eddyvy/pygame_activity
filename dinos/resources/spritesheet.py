from dinos.resources.asset_manager import AssetManager


class SpriteSheet:

    def __init__(self, image_name):
        self.__image = AssetManager.instance().image.get()
