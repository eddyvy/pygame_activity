from sre_parse import State

import pygame
from dinos.config import Config
from dinos.intro.intro_menu import IntroMenu
from dinos.resources.asset_manager import AssetManager
from dinos.resources.sound_player import SoundPlayer

from dinos.state.state import StateTypes


class IntroState(State):
    __STATE = StateTypes.Intro

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.GamePlay

    def enter(self):
        self.done = False

        self.__load_assets()
        self.__menu = IntroMenu(self.__accept, self.__exit)
        SoundPlayer.instance().play_music(Config.get("intro", "music"))

    def handle_event(self, event):
        self.__menu.handle_event(event)

    def update(self, delta_time):
        self.__menu.update(delta_time)
        SoundPlayer.instance().update(delta_time)

    def render(self, surface):
        self.__menu.render(surface)

    def quit(self):
        self.__menu.quit()
        self.__unload_assets()

    def __load_assets(self):
        AssetManager.instance().font.load(
            self.__STATE,
            Config.get("intro", "font")
        )
        AssetManager.instance().music.load(self.__STATE, Config.get("intro", "music"))
        AssetManager.instance().sfx.load(self.__STATE, Config.get("intro", "sfx_select"))

    def __unload_assets(self):
        AssetManager.instance().clean(self.__STATE)

    def __accept(self):
        self.done = True

    def __exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
