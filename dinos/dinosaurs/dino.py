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

        self.is_hit = False
        self._is_hit_dir = "right"
        self.__hit_speed_x = Config.get("game_play", "dinos", "hit_speed")[0]
        self.__hit_speed_y = Config.get("game_play", "dinos", "hit_speed")[1]
        self.__hit_duration = Config.get("game_play", "dinos", "hit_duration")
        self.__hit_cooldown = 0

        self.__get_target_pos = get_target_pos_cb

        self.is_dying = False
        self.__dying_time = Config.get("game_play", "dinos", "dying_time")
        self.__die_callback = None

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

        self.is_hit = False
        self._hit_dir = "right"

        self.is_dying = False
        self.__dying_time = Config.get("game_play", "dinos", "dying_time")
        self.__die_callback = None

        self.position.x = newpos[0]
        self.position.y = newpos[1]
        self._center()

    def update(self, delta_time):
        if self.is_dying:
            self.__dying_time -= delta_time
            if self.__dying_time <= 0:
                self.__die_callback(self)
        else:
            if random.random() <= self.__jump_prob:
                self.__jump()

            self.__update_movement(delta_time)

        super().update(delta_time)

    def is_touching_ground(self):
        self.__is_on_air = self._is_jumping

    def die(self, callback):
        self.is_dying = True
        self.__die_callback = callback
        SoundPlayer.instance().play_sound("dead_enemy")

    def hit(self, direction):
        self.is_hit = True
        self._hit_dir = direction
        self.__hit_cooldown = self.__hit_duration

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

        if self.is_hit:
            if self.__hit_cooldown <= 0:
                self.is_hit = False
            else:
                self.__hit_cooldown -= delta_time
            self._velocity.x = self.__hit_speed_x if self._hit_dir == "left" else -self.__hit_speed_x
            self._velocity.y = - self.__hit_speed_y
            self.__is_on_air = True

        self.position += self._velocity * delta_time
