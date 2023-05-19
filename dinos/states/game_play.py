from sre_parse import State
from dinos.config import Config

from dinos.modes.mode import Mode
from dinos.resources.font_manager import FontManager
from dinos.states.state import StateTypes
from dinos.ui.fps_stats import FPSStats


class GamePlay(State):

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

    def enter(self):
        self.done = False
        self.__fps_stats = FPSStats()
        self.__load_assets()
        self.__mode = Mode()

    def handle_event(self, event):
        self.__mode.handle_event(event)

    def update(self, delta_time):
        if self.__mode.debug:
            self.__fps_stats.update(delta_time)

        if self.__mode.pause:
            pass

    def render(self, surface):
        if self.__mode.debug:
            self.__fps_stats.render(surface)

        if self.__mode.pause:
            pass

    def quit(self):
        self.__unload_assets()
        self.__mode.quit()

    def __load_assets(self):
        pass

    def __unload_assets(self):
        pass
