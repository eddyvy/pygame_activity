from dinos.common.game_abstract import Renderable, Updatable
from dinos.config import Config
from dinos.resources.asset_manager import AssetManager
from dinos.ui.label import UILabel


class GamePlayHUD(Updatable, Renderable):

    def __init__(self, get_kills_callback, get_bullets_callback):
        self.__get_kills = get_kills_callback
        self.__get_bullets = get_bullets_callback

        kills_data = Config.get("game_play", "hud", "kills")
        kills_font = AssetManager.instance().font.get(kills_data["font"])
        self.__kills_label = UILabel(
            kills_font,
            str(get_kills_callback()),
            (kills_data["position"][0],
             kills_data["position"][1]),
            kills_data["font_color"]
        )

        bullets_data = Config.get("game_play", "hud", "bullets")
        bullets_font = AssetManager.instance().font.get(bullets_data["font"])
        self.__bullet_image = AssetManager.instance(
        ).image.get(bullets_data["image"])
        self.__bullets_rect = self.__bullet_image.get_rect()
        self.__bullets_rect.x = bullets_data["image_position"][0]
        self.__bullets_rect.y = bullets_data["image_position"][1]
        self.__bullet_label = UILabel(
            bullets_font,
            str(get_bullets_callback()),
            (bullets_data["font_position"][0],
             bullets_data["font_position"][1]),
            bullets_data["font_color"]
        )

    def update(self, delta_time):
        self.__kills_label.set_text(str(self.__get_kills()))
        self.__bullet_label.set_text(str(self.__get_bullets()))

    def render(self, surface):
        self.__kills_label.render(surface)
        self.__bullet_label.render(surface)
        surface.blit(self.__bullet_image, self.__bullets_rect)

    def quit(self):
        pass
