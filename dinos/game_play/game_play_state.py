from sre_parse import State

import pygame
from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.environment.platform import Platform

from dinos.game_play.game_play_mode import GamePlayMode
from dinos.hero.hero import Hero
from dinos.resources.asset_manager import AssetManager
from dinos.resources.sound_player import SoundPlayer
from dinos.state.state import StateTypes
from dinos.game_play.fps_stats import FPSStats


class GamePlayState(State):
    __STATE = StateTypes.GamePlay

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

        self.__platforms = RenderGroup()

    def enter(self):
        self.done = False
        self.__load_assets()
        self.__mode = GamePlayMode.instance()
        self.__fps_stats = FPSStats()

        self.__platforms.add(Platform(
            Config.get("game_play", "environment", "ground", "position"),
            Config.get("game_play", "environment", "ground", "tiles_width")
        ))
        self.__player = Hero(
            Config.get("game_play", "hero", "spawn_position"))
        SoundPlayer.instance().play_music_fade(Config.get("game_play", "music"))

    def handle_event(self, event):
        self.__mode.handle_event(event)

        if self.__mode.pause:
            return

        self.__player.handle_event(event)

    def update(self, delta_time):
        SoundPlayer.instance().update(delta_time)
        if self.__mode.debug:
            self.__fps_stats.update(delta_time)

        if self.__mode.pause:
            return

        self.__player.update(delta_time)

        for platform in pygame.sprite.spritecollide(self.__player, self.__platforms, False):
            prev_feet = self.__player.prev_rect.bottom
            feet = self.__player.rect.bottom
            if (
                (feet >= platform.rect.top and feet <= platform.rect.bottom)
                or (feet >= platform.rect.bottom and prev_feet <= platform.rect.top)
            ):
                self.__player.is_touching_ground()

    def render(self, surface):
        if self.__mode.debug:
            self.__fps_stats.render(surface)

        if self.__mode.pause:
            pass

        self.__platforms.render(surface)
        self.__player.render(surface)

    def quit(self):
        SoundPlayer.instance().stop_music()
        self.__player.kill()
        self.__platforms.empty()
        self.__mode.quit()
        self.__fps_stats.quit()
        self.__unload_assets()

    def __load_assets(self):
        AssetManager.instance().font.load(
            self.__STATE,
            Config.get("game_play", "fps_stats", "fps_font")
        )
        AssetManager.instance().music.load(
            self.__STATE,
            Config.get("game_play", "music")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "hero", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "platform", "spritesheet")
        )

    def __unload_assets(self):
        AssetManager.instance().clean(StateTypes.GamePlay)
