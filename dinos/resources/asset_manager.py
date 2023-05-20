from importlib import resources
from os import path

from dinos.resources.font_manager import FontManager
from dinos.resources.image_manager import ImageManager
from dinos.resources.music_manager import MusicManager
from dinos.resources.sfx_manager import SfxManager
from dinos.resources.spritesheet_manager import SpriteSheetManager


class AssetManager:

    __instance = None

    @staticmethod
    def instance():
        if AssetManager.__instance is None:
            AssetManager()
        return AssetManager.__instance

    def __init__(self):
        if not AssetManager.__instance is None:
            raise Exception("There Can Be Only One AssetManager!!!")
        AssetManager.__instance = self

        self.font = FontManager()
        self.image = ImageManager()
        self.music = MusicManager()
        self.spritesheet = SpriteSheetManager()
        self.sfx = SfxManager()

    def clean(self, state):
        self.font.clean(state)
        self.image.clean(state)
        self.music.clean(state)
        self.spritesheet.clean(state)
        self.sfx.clean(state)
