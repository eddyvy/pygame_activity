import pygame
from dinos.config import Config
from dinos.dinosaurs.dino_body import DinoBody
from dinos.resources.sound_player import SoundPlayer


class Dino(DinoBody):

    def __init__(self):
        inipos = (300, 400)
        super().__init__(inipos)

        self._speed = Config.get("game_play", "dinos", "speed")
        self._jump_speed = Config.get("game_play", "dinos", "jump_speed")
        self.__gravity = Config.get("game", "physics", "gravity")
        self.__max_falling_speed = Config.get(
            "game", "physics", "max_falling_speed")

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self._is_moving_left = False
        self._is_moving_right = False
        self.__is_on_air = True
        self.__is_jumping = False
        self.__heading_dir = "right"

        self._center()

    def update(self, delta_time):
        self.__update_movement(delta_time)
        super().update(delta_time)

    def is_touching_ground(self):
        self.__is_on_air = self.__is_jumping

    def __update_movement(self, delta_time):
        self._velocity.x = 0

        if self._is_moving_left:
            self._velocity.x -= self._speed
        if self._is_moving_right:
            self._velocity.x += self._speed

        if self.__is_on_air:
            self._velocity.y += self.__gravity
            if self._velocity.y > self.__max_falling_speed:
                self._velocity.y = self.__max_falling_speed
            if self.__is_jumping and self._velocity.y <= 0:
                self.__is_jumping = False
        else:
            if self.__is_jumping:
                self._velocity.y = -self._jump_speed
                self.__is_on_air = True
                SoundPlayer.instance().play_sound("jump_enemy")
            else:
                self._velocity.y = 0

        distance = self._velocity * delta_time

        self.position.y += distance.y
