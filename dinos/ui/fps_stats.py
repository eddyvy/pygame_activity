from dinos.common.game_abstract import Renderable, Updatable
from dinos.config import Config
from dinos.resources.font_manager import FontManager
from dinos.states.state import StateTypes


class FPSStats(Updatable, Renderable):

    def __init__(self):
        self.__logic_frames = 0
        self.__render_frames = 0
        self.__update_time = 0
        self.__set_fps_surface()
        self.__refresh_update_time = Config.get(
            "timing", "refresh_update_time")

    def update(self, delta_time):
        self.__update_time += delta_time
        self.__logic_frames += 1

        if self.__update_time > self.__refresh_update_time:
            self.__set_fps_surface()
            self.__logic_frames = 0
            self.__render_frames = 0
            self.__update_time -= self.__refresh_update_time

    def render(self, surface_dst):
        self.__render_frames += 1
        surface_dst.blit(self.__image, Config.get("timing", "fps_pos"))

    def quit(self):
        pass

    def __set_fps_surface(self):
        font = FontManager.instance().get(
            StateTypes.Global, Config.get("fonts", "main", "name"))
        self.__image = font.render(
            f"{self.__logic_frames} - {self.__render_frames}", True, Config.get("fonts", "main", "color"), None)
