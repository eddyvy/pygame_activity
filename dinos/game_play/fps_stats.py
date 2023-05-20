from dinos.common.game_abstract import Renderable, Updatable
from dinos.config import Config
from dinos.resources.font_manager import FontManager
from dinos.state.state import StateTypes
from dinos.ui.label import UILabel


class FPSStats(Updatable, Renderable):

    def __init__(self):
        self.__logic_frames = 0
        self.__render_frames = 0
        self.__update_time = 0

        font = FontManager.instance().get(
            StateTypes.Global,
            Config.get("fonts", "main", "name")
        )

        self.__label = UILabel(
            font,
            "0 - 0",
            Config.get("timing", "fps_pos"),
            Config.get("game", "foreground_color"),
            Config.get("game", "background_color")
        )

        self.__refresh_update_time = Config.get(
            "timing", "refresh_update_time")

    def update(self, delta_time):
        self.__update_time += delta_time
        self.__logic_frames += 1

        if self.__update_time > self.__refresh_update_time:
            self.__set_text()
            self.__logic_frames = 0
            self.__render_frames = 0
            self.__update_time -= self.__refresh_update_time

    def render(self, surface):
        self.__render_frames += 1
        self.__label.render(surface)

    def quit(self):
        pass

    def __set_text(self):
        self.__label.set_text(
            f"{self.__logic_frames} - {self.__render_frames}"
        )
