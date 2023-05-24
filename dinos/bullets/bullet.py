import pygame
from dinos.common.game_object import GameObject
from dinos.config import Config
from dinos.game_play.game_play_mode import GamePlayMode
from dinos.resources.asset_manager import AssetManager


class Bullet(GameObject):

    def __init__(self):
        super().__init__()
        self.__image = AssetManager.instance().image.get(
            Config.get("game_play", "bullet", "image"))

        self.rect = self.__image.get_rect().copy()
        self.render_rect = self.rect.copy()
        self._center()

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self.__speed = Config.get("game_play", "bullet", "speed")
        self.__is_moving = False

        self.__target = pygame.math.Vector2(0.0, 0.0)
        self.__arrive_radius = Config.get(
            "game_play", "bullet", "arrive_radius")

    def reset(self):
        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self.__is_moving = False
        self.__target = pygame.math.Vector2(0.0, 0.0)

    def handle_event(self, event):
        pass

    def update(self, delta_time):
        if self.__is_moving:
            dif = self.__target - self.position

            if dif.length_squared() < self.__arrive_radius:
                self._velocity.x = 0
                self._velocity.y = 0
                self.__is_moving = False
            else:
                self._velocity = (dif).normalize() * self.__speed

            self.position += self._velocity * delta_time

        self._center()

    def render(self, surface):
        surface.blit(self.__image, self.render_rect)

        if GamePlayMode.instance().debug:
            self._render_debug(surface)

    def quit(self):
        self.kill()

    def move(self, to_pos):
        self.__is_moving = True
        self.__target = to_pos
