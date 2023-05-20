from sre_parse import State
from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.environment.platform import Platform

from dinos.game_play.game_play_mode import GamePlayMode
from dinos.hero.hero import Hero
from dinos.resources.asset_manager import AssetManager
from dinos.state.state import StateTypes
from dinos.game_play.fps_stats import FPSStats


class GamePlayState(State):
    __STATE = StateTypes.GamePlay

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

        self.__platforms = RenderGroup()
        self.__entities = RenderGroup()

    def enter(self):
        self.done = False
        self.__load_assets()
        self.__mode = GamePlayMode()
        self.__fps_stats = FPSStats()

        self.__ground = Platform(
            Config.get("game_play", "environment", "ground", "position"),
            Config.get("game_play", "environment", "ground", "tiles_width")
        )
        self.__entities.add(Hero())

    def handle_event(self, event):
        self.__mode.handle_event(event)

        if self.__mode.pause:
            return

        self.__entities.handle_event(event)

    def update(self, delta_time):
        if self.__mode.debug:
            self.__fps_stats.update(delta_time)

        if self.__mode.pause:
            return

        self.__entities.update(delta_time)

    def render(self, surface):
        if self.__mode.debug:
            self.__fps_stats.render(surface)

        if self.__mode.pause:
            pass

        self.__ground.render(surface)
        self.__entities.render(surface)

    def quit(self):
        self.__entities.empty()
        self.__mode.quit()
        self.__fps_stats.quit()
        self.__unload_assets()

    def __load_assets(self):
        AssetManager.instance().font.load(
            self.__STATE,
            Config.get("game_play", "fps_stats", "fps_font")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "hero", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "environment", "ground", "spritesheet")
        )

    def __unload_assets(self):
        AssetManager.instance().clean(StateTypes.GamePlay)
