import pygame

from dinos.common.game_object import GameObject
from dinos.common.input_key_map import InputKeyMap
from dinos.config import Config
from dinos.resources.animations_handler import AnimationsHandler
from dinos.resources.asset_manager import AssetManager


class Hero(GameObject):

    def __init__(self):
        super().__init__()

        self.__inputs = InputKeyMap("hero")

        self.__animations = AnimationsHandler(
            Config.get("game_play", "hero", "animations"),
            "idle_right"
        )
        _, clip = self.__animations.get_current_image()

        print(clip)

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

        self.__velocity = pygame.math.Vector2(0.0, 0.0)
        self.__is_moving_left = False
        self.__is_moving_right = False

        self._center()

    def handle_event(self, event):
        if self.__inputs.is_pressed(event, "left"):
            self.__is_moving_left = True
        if self.__inputs.is_released(event, "left"):
            self.__is_moving_left = False
        if self.__inputs.is_pressed(event, "right"):
            self.__is_moving_right = True
        if self.__inputs.is_released(event, "right"):
            self.__is_moving_right = False

    def update(self, delta_time):
        self.__velocity.x = 0
        self.__velocity.y = 0

        if self.__is_moving_left:
            self.__velocity.x -= Config.get("game_play", "hero", "speed")
        if self.__is_moving_right:
            self.__velocity.x += Config.get("game_play", "hero", "speed")

        distance = self.__velocity * delta_time

        if self.__check_bounds(self.__velocity):
            self._position += distance

        self.__update_animations(delta_time)
        self._center()

    def render(self, surface):
        image, clip = self.__animations.get_current_image()
        surface.blit(image, self._render_rect, clip)

    def quit(self):
        pass

    def __check_bounds(self, velocity):
        new_pos = self._position + velocity

        if (
            new_pos.x < 0
            or new_pos.x > Config.get("game", "screen_size")[0]
            or new_pos.y < self.render_rect.height/2
            or new_pos.y > Config.get("game", "screen_size")[1] - self.render_rect.height/2
        ):
            return False

        return True

    def __update_animations(self, delta_time):
        if self.__velocity.x < 0:
            self.__animations.animate("walk_left")
        elif self.__velocity.x > 0:
            self.__animations.animate("walk_right")
        elif self.__velocity.x == 0:
            if self.__animations.get_current_animation_name() == "walk_left":
                self.__animations.animate("idle_left")
            elif self.__animations.get_current_animation_name() == "walk_right":
                self.__animations.animate("idle_right")

        self.__animations.update(delta_time)
