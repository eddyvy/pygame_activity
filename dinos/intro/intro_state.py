from sre_parse import State

import pygame
from dinos.intro.intro_menu import IntroMenu

from dinos.state.state import StateTypes


class IntroState(State):

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.GamePlay

    def enter(self):
        self.done = False
        self.__menu = IntroMenu(self.__accept, self.__exit)
        self.__load_assets()

    def handle_event(self, event):
        self.__menu.handle_event(event)

    def update(self, delta_time):
        self.__menu.update(delta_time)

    def render(self, surface):
        self.__menu.render(surface)

    def quit(self):
        self.__menu.quit()
        self.__unload_assets()

    def __load_assets(self):
        pass

    def __unload_assets(self):
        pass

    def __accept(self):
        self.done = True

    def __exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
