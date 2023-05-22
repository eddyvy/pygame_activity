import random
import pygame
from dinos.config import Config
from dinos.dinosaurs.dino_body import DinoBody
from dinos.resources.sound_player import SoundPlayer


class Dino(DinoBody):

    def __init__(self, get_target_pos_cb):
        initial_position = Config.get("game_play", "dinos", "spawn_pos_left") if random.randint(
            0, 1) == 0 else Config.get("game_play", "dinos", "spawn_pos_right")

        super().__init__(initial_position)

        self.__max_speed = Config.get(
            "game_play", "dinos", "max_speed") * (1 + random.random())
        self.__acceleration = Config.get(
            "game_play", "dinos", "acceleration") * (1 + random.random())
        self.__jump_prob = Config.get(
            "game_play", "dinos", "jump_prob") * (1 + random.random())

        self._jump_speed = Config.get("game_play", "dinos", "jump_speed")
        self.__distance_to_jump = Config.get(
            "game_play", "dinos", "distance_to_jump")
        self.__gravity = Config.get("game", "physics", "gravity")
        self.__max_falling_speed = Config.get(
            "game", "physics", "max_falling_speed")

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self._is_jumping = False
        self.__is_on_air = True

        self.__get_target_pos = get_target_pos_cb

        self._center()

    def reset(self):
        newpos = Config.get("game_play", "dinos", "spawn_pos_left") if random.randint(
            0, 1) == 0 else Config.get("game_play", "dinos", "spawn_pos_right")

        self.__max_speed = Config.get(
            "game_play", "dinos", "max_speed") * (1 + random.random())
        self.__acceleration = Config.get(
            "game_play", "dinos", "acceleration") * (1 + random.random())
        self.__jump_prob = Config.get(
            "game_play", "dinos", "jump_prob") * (1 + random.random())

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self._is_jumping = False
        self.__is_on_air = True

        self.position.x = newpos[0]
        self.position.y = newpos[1]
        self._center()

    def update(self, delta_time):
        if random.random() <= self.__jump_prob:
            self.__jump()

        self.__update_movement(delta_time)
        super().update(delta_time)

    def is_touching_ground(self):
        self.__is_on_air = self._is_jumping

    def __jump(self):
        if not self.__is_on_air:
            self._is_jumping = True

    def __update_movement(self, delta_time):
        self._velocity.x += (
            self.__get_target_pos().x -
            self.position.x
        ) * self.__acceleration
        if (abs(self._velocity.x) >= self.__max_speed):
            self._velocity.x = self.__max_speed if self._velocity.x > 0 else -self.__max_speed

        if (
            (self.__get_target_pos().y < self.rect.top) and
            (abs(self.__get_target_pos().x - self.position.x)
             < self.__distance_to_jump)
        ):
            self.__jump()

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
