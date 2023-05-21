from dinos.common.game_abstract import EventHandler
from dinos.common.input_key_map import InputKeyMap


class GamePlayMode(EventHandler):

    __instance = None

    @staticmethod
    def instance():
        if GamePlayMode.__instance is None:
            GamePlayMode()
        return GamePlayMode.__instance

    def __init__(self):
        if not GamePlayMode.__instance is None:
            raise Exception("There Can Be Only One GamePlayMode!!!")
        GamePlayMode.__instance = self

        self.__inputs = InputKeyMap("mode")
        self.debug = False
        self.pause = False

    def handle_event(self, event):
        if self.__inputs.is_pressed(event, "debug"):
            self.debug = not self.debug

        if self.__inputs.is_pressed(event, "pause"):
            self.pause = not self.pause

    def quit(self):
        pass
