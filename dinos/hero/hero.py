import pygame

from dinos.common.game_object import GameObject
from dinos.common.input_key_map import InputKeyMap
from dinos.config import Config
from dinos.game_play.game_play_mode import GamePlayMode
from dinos.resources.animations_handler import AnimationsHandler
from dinos.resources.asset_manager import AssetManager


class Hero(GameObject):

    def __init__(self, position):
        super().__init__()

        self.__inputs = InputKeyMap("hero")

        self.__animations = AnimationsHandler(
            Config.get("game_play", "hero", "animations"),
            "idle_right"
        )
        _, clip = self.__animations.get_current_image()

        self.rect = clip.copy()
        self.render_rect = self.rect.copy()
        self.position = pygame.math.Vector2(position)

        self._render_offset = pygame.math.Vector2(
            *Config.get("game_play", "hero", "render_offset"))

        infco = Config.get("game_play", "hero", "inflate_collider")
        self.rect.inflate_ip(
            self.rect.width * infco[0],
            self.rect.height * infco[1]
        )
        self.prev_rect = self.rect.copy()

        self.__speed = Config.get("game_play", "hero", "speed")
        self.__jump_speed = Config.get("game_play", "hero", "jump_speed")
        self.__velocity = pygame.math.Vector2(0.0, 0.0)
        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__is_falling = True
        self.__is_jumping = False

        self._center()

    def handle_event(self, event):
        if self.__inputs.is_released(event, "left"):
            self.__is_moving_left = False
        if self.__inputs.is_released(event, "right"):
            self.__is_moving_right = False
        if self.__inputs.is_pressed(event, "left"):
            self.__is_moving_left = True
            self.__is_moving_right = False
        if self.__inputs.is_pressed(event, "right"):
            self.__is_moving_right = True
            self.__is_moving_left = False
        if self.__inputs.is_pressed(event, "jump"):
            if not self.__is_falling:
                self.__is_jumping = True

    def update(self, delta_time):
        self.__update_movement(delta_time)
        self.__update_animations(delta_time)
        self._center()

    def render(self, surface: pygame.Surface):
        image, clip = self.__animations.get_current_image()
        surface.blit(image, self.render_rect, clip)

        if GamePlayMode.instance().debug:
            self._render_debug(surface)

    def quit(self):
        pass

    def is_touching_ground(self):
        self.__is_falling = self.__is_jumping

    def __check_bounds(self, velocity):
        new_pos = self.position + velocity
        return not (
            new_pos.x < 0
            or new_pos.x > Config.get("game", "screen_size")[0]
        )

    def __update_movement(self, delta_time):
        self.__velocity.x = 0

        if self.__is_moving_left:
            self.__velocity.x -= self.__speed
        if self.__is_moving_right:
            self.__velocity.x += self.__speed

        if self.__is_falling:
            self.__velocity.y += Config.get("game", "physics", "gravity")
            if self.__velocity.y > Config.get("game", "physics", "max_falling_speed"):
                self.__velocity.y = Config.get(
                    "game", "physics", "max_falling_speed")
            if self.__is_jumping and self.__velocity.y <= 0:
                self.__is_jumping = False
        else:
            if self.__is_jumping:
                self.__velocity.y = -self.__jump_speed
                self.__is_falling = True
            else:
                self.__velocity.y = 0

        distance = self.__velocity * delta_time

        if self.__check_bounds(self.__velocity):
            self.position.x += distance.x

        self.position.y += distance.y

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
