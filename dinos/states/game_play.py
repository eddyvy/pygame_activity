from sre_parse import State
from dinos.modes.mode_manager import ModeManager

from dinos.states.state_types import StateTypes


class GamePlay(State):

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

    def enter(self):
        self.done = False
        self.__load_assets()
        self.__mode = ModeManager()

    def handle_event(self, event):
        self.__mode.handle_event(event)

    def update(self, delta_time):
        if self.__mode.debug:
            print("Debug mode")

        if self.__mode.pause:
            print("Pause mode")

    def render(self, surface):
        pass

    def quit(self):
        self.__unload_assets()
        self.__mode.quit()

    def __load_assets(self):
        pass

    def __unload_assets(self):
        pass
