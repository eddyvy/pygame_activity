import random
import pygame
from dinos.config import Config
from dinos.dinosaurs.dino_body import DinoBody
from dinos.resources.sound_player import SoundPlayer


class Dino(DinoBody):

    def __init__(self, get_target_pos_cb):
        inipos = (300, 400)
        super().__init__(inipos)

        self.__max_speed = Config.get("game_play", "dinos", "max_speed")
        self.__acceleration = Config.get("game_play", "dinos", "acceleration")
        self._jump_speed = Config.get("game_play", "dinos", "jump_speed")
        self.__gravity = Config.get("game", "physics", "gravity")
        self.__max_falling_speed = Config.get(
            "game", "physics", "max_falling_speed")

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self._is_jumping = False
        self.__is_on_air = True

        self.__get_target_post = get_target_pos_cb

        self._center()

    def update(self, delta_time):
        if random.randint(0, 50) == 0:
            self.__jump()

        self.__update_movement(delta_time)
        super().update(delta_time)

    def is_touching_ground(self):
        self.__is_on_air = self._is_jumping

    def __jump(self):
        if not self.__is_on_air:
            self._is_jumping = True
            SoundPlayer.instance().play_sound("jump_enemy")

    def __update_movement(self, delta_time):
        self._velocity.x += (
            self.__get_target_post().x -
            self.position.x
        ) * self.__acceleration
        if (abs(self._velocity.x) >= self.__max_speed):
            self._velocity.x = self.__max_speed if self._velocity.x > 0 else -self.__max_speed

        if self.__is_on_air:
            self._velocity.y += self.__gravity
            if self._velocity.y > self.__max_falling_speed:
                self._velocity.y = self.__max_falling_speed
            if self._is_jumping and self._velocity.y <= 0:
                self._is_jumping = False
        else:
            if self._is_jumping:
                self._velocity.y = -self._jump_speed
                self.__is_on_air = True
            else:
                self._velocity.y = 0

        self.position += self._velocity * delta_time
