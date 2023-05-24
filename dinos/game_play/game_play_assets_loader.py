from dinos.config import Config
from dinos.resources.asset_manager import AssetManager
from dinos.state.state import StateTypes


class GamePlayAssetsLoader:
    def __init__(self):
        self.__state = StateTypes.GamePlay

    def load(self):
        AssetManager.instance().font.load(
            self.__state,
            Config.get("game_play", "fps_stats", "fps_font")
        )
        AssetManager.instance().font.load(
            self.__state,
            Config.get("game_play", "hud", "kills", "font")
        )
        AssetManager.instance().font.load(
            self.__state,
            Config.get("game_play", "hud", "bullets", "font")
        )
        AssetManager.instance().image.load(
            self.__state,
            Config.get("game_play", "environment", "background", "image")
        )
        AssetManager.instance().image.load(
            self.__state,
            Config.get("game_play", "hud", "bullets", "image"),
        )
        AssetManager.instance().image.load(
            self.__state,
            Config.get("game_play", "bullet", "image")
        )
        AssetManager.instance().music.load(
            self.__state,
            Config.get("game_play", "music")
        )
        for sfx in Config.get("game_play", "sfx"):
            AssetManager.instance().sfx.load(self.__state, sfx)
        AssetManager.instance().spritesheet.load(
            self.__state,
            Config.get("game_play", "hero", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__state,
            Config.get("game_play", "platform", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__state,
            Config.get("game_play", "dinos", "spritesheet")
        )

    def unload(self):
        AssetManager.instance().clean(StateTypes.GamePlay)
