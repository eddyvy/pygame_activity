from dinos.common.game_abstract import Renderable, Updatable
from dinos.config import Config
from dinos.resources.animations_handler import AnimationsHandler
from dinos.resources.asset_manager import AssetManager
from dinos.ui.label import UILabel


class IntroTutorial(Updatable, Renderable):

    def __init__(self):
        tuto_data = Config.get("intro", "tutorial")

        font = AssetManager.instance().font.get(Config.get("intro", "font"))
        fg_c = Config.get("game", "foreground_color")

        self.__jump_animation = AnimationsHandler(
            tuto_data["animations"], tuto_data["jump"]["animation"])
        _, clip = self.__jump_animation.get_current_image()
        self.__jump_rect = clip.copy()
        self.__jump_rect.x = tuto_data["jump"]["position"][0]
        self.__jump_rect.y = tuto_data["jump"]["position"][1]
        jump_text_pos = tuto_data["jump"]["text_position"]
        jump_input_text = " ".join(Config.get("input", "hero", "jump")).upper()
        self.__jump_text = UILabel(font, jump_input_text, jump_text_pos, fg_c)

        self.__hit_animation = AnimationsHandler(
            tuto_data["animations"], tuto_data["hit"]["animation"])
        _, clip = self.__hit_animation.get_current_image()
        self.__hit_rect = clip.copy()
        self.__hit_rect.x = tuto_data["hit"]["position"][0]
        self.__hit_rect.y = tuto_data["hit"]["position"][1]
        hit_text_pos = tuto_data["hit"]["text_position"]
        hit_input_text = " ".join(Config.get("input", "hero", "hit")).upper()
        self.__hit_text = UILabel(font, hit_input_text, hit_text_pos, fg_c)

        self.__shoot_animation = AnimationsHandler(
            tuto_data["animations"], tuto_data["shoot"]["animation"])
        _, clip = self.__shoot_animation.get_current_image()
        self.__shoot_rect = clip.copy()
        self.__shoot_rect.x = tuto_data["shoot"]["position"][0]
        self.__shoot_rect.y = tuto_data["shoot"]["position"][1]
        shoot_text_pos = tuto_data["shoot"]["text_position"]
        shoot_input_text = " ".join(
            Config.get("input", "hero", "shoot")).upper()
        self.__shoot_text = UILabel(
            font, shoot_input_text, shoot_text_pos, fg_c)

    def update(self, delta_time):
        self.__jump_animation.update(delta_time)
        self.__hit_animation.update(delta_time)
        self.__shoot_animation.update(delta_time)

    def render(self, surface):
        image, clip = self.__jump_animation.get_current_image()
        surface.blit(image, self.__jump_rect, clip)
        image, clip = self.__hit_animation.get_current_image()
        surface.blit(image, self.__hit_rect, clip)
        image, clip = self.__shoot_animation.get_current_image()
        surface.blit(image, self.__shoot_rect, clip)
        self.__jump_text.render(surface)
        self.__hit_text.render(surface)
        self.__shoot_text.render(surface)

    def quit(self):
        pass
