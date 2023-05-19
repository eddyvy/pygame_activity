from dinos.common.game_abstract import EventHandler
from dinos.common.input_key_map import InputKeyMap


class Mode(EventHandler):

    __DEBUG = "debug"
    __PAUSE = "pause"

    def __init__(self):
        self.__inputs = InputKeyMap("mode")
        self.debug = False
        self.pause = False

    def handle_event(self, event):
        if self.__inputs.is_pressed(event, self.__DEBUG):
            self.debug = not self.debug

        if self.__inputs.is_pressed(event, self.__PAUSE):
            self.pause = not self.pause

    def quit(self):
        pass
