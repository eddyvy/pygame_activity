import pygame

from dinos.common.game_object import GameObject
from dinos.config import Config
from dinos.resources.animations_handler import AnimationsHandler
from dinos.resources.asset_manager import AssetManager


class Hero(GameObject):

    def __init__(self):
        super().__init__()

        self.__animations = AnimationsHandler(
            Config.get("game_play", "hero", "animations"),
            "idle_right"
        )
        _, clip = self.__animations.get_current_image()

        self.rect = clip.copy()
        self.render_rect = self.rect.copy()

        self._position = pygame.math.Vector2(
            Config.get("game", "screen_size")[0]/2,
            500 - clip.h
        )

        infco = Config.get("game_play", "hero", "inflate_collider")
        self.rect.inflate_ip(
            self.rect.width * infco[0],
            self.rect.height * infco[1]
        )

    def handle_event(self, event):
        pass

    def update(self, delta_time):
        self.__animations.update(delta_time)
        self._center()

    def render(self, surface):
        image, clip = self.__animations.get_current_image()
        surface.blit(image, self._render_rect, clip)

    def quit(self):
        pass
