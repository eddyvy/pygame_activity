from sre_parse import State

from dinos.states.state_types import StateTypes


class GamePlay(State):

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

    def enter(self):
        self.done = False
        self.__load_assets()

    def handle_event(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface):
        pass

    def quit(self):
        self.__unload_assets()

    def __load_assets(self):
        pass

    def __unload_assets(self):
        pass
