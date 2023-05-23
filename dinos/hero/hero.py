import pygame

from dinos.common.input_key_map import InputKeyMap
from dinos.config import Config
from dinos.hero.hero_body import HeroBody
from dinos.resources.sound_player import SoundPlayer


class Hero(HeroBody):

    def __init__(self, position):
        super().__init__(position)

        self._inputs = InputKeyMap("hero")

        self._speed = Config.get("game_play", "hero", "speed")
        self._jump_speed = Config.get("game_play", "hero", "jump_speed")
        self.__gravity = Config.get("game", "physics", "gravity")
        self.__max_falling_speed = Config.get(
            "game", "physics", "max_falling_speed")
        self.__shoot_cd = Config.get("game_play", "hero", "shoot_cd")
        self.__shoot_offset = Config.get("game_play", "hero", "shoot_offset")
        self.__hit_cd = Config.get("game_play", "hero", "hit_cd")
        self.__hit_width = Config.get("game_play", "hero", "hit_width")
        self.__hit_height = Config.get("game_play", "hero", "hit_height")

        self._velocity = pygame.math.Vector2(0.0, 0.0)
        self._is_moving_left = False
        self._is_moving_right = False
        self.__is_on_air = True
        self.__is_jumping = False
        self.__heading_dir = "right"

        self._is_shooting = False
        self.__shoot_cooldown = 0
        self.__shoot_callback = None
        self.__shoot_dir = self.__heading_dir

        self.is_hitting = False
        self.__hit_cooldown = 0
        self.__hit_callback = None
        self.__hit_dir = self.__heading_dir
        self.hit_rect = pygame.Rect(0, 0, 0, 0)
        self.hit_rect.center = self.rect.center

        self._center()

    def handle_event(self, event):
        if self._inputs.is_released(event, "left"):
            self._is_moving_left = False
        if self._inputs.is_released(event, "right"):
            self._is_moving_right = False
        if self._inputs.is_pressed(event, "left"):
            self._is_moving_left = True
            self._is_moving_right = False
            self.__heading_dir = "left"
        if self._inputs.is_pressed(event, "right"):
            self._is_moving_right = True
            self._is_moving_left = False
            self.__heading_dir = "right"
        if self._inputs.is_pressed(event, "jump"):
            self.__jump()
        if self._inputs.is_pressed(event, "shoot"):
            self.__shoot()
        if self._inputs.is_pressed(event, "hit"):
            self.__hit()

    def update(self, delta_time):
        self.__update_movement(delta_time)
        self.__update_hitting(delta_time)
        self.__update_shooting(delta_time)
        super().update(delta_time)

    def is_touching_ground(self):
        self.__is_on_air = self.__is_jumping

    def set_shoot_action(self, shoot_callback):
        self.__shoot_callback = shoot_callback

    def set_hit_action(self, hit_callback):
        self.__hit_callback = hit_callback

    def __jump(self):
        if not self.__is_on_air:
            self.__is_jumping = True
            SoundPlayer.instance().play_sound("jump")

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
            else:
                self._velocity.y = 0

        distance = self._velocity * delta_time

        if self.__check_bounds(self._velocity):
            self.position.x += distance.x

        self.position.y += distance.y

    def __check_bounds(self, velocity):
        new_pos = self.position + velocity
        return not (
            new_pos.x < 0
            or new_pos.x > Config.get("game", "screen_size")[0]
        )

    def __shoot(self):
        if self.__shoot_cooldown > 0 or self.__shoot_callback == None or self.is_hitting:
            return

        self.__shoot_dir = self.__heading_dir
        if self.__shoot_callback(
            (int(self.position.x), int((self.position.y) - self.__shoot_offset)),
            self.__shoot_dir
        ):
            self._is_shooting = True
            self.__shoot_cooldown = self.__shoot_cd

    def __update_shooting(self, delta_time):
        if not self._is_shooting:
            return
        self.__shoot_cooldown -= delta_time
        if self.__shoot_cooldown <= 0:
            self._is_shooting = False

    def __hit(self):
        if self.__hit_cooldown > 0 or self.__hit_callback == None or self._is_shooting:
            return

        self.__hit_dir = self.__heading_dir

        self.hit_rect.w = self.__hit_width
        self.hit_rect.h = self.__hit_height
        if self.__hit_dir == "right":
            self.hit_rect.left = self.rect.right
        elif self.__hit_dir == "left":
            self.hit_rect.right = self.rect.left

        if self.__hit_callback(self.hit_rect):
            self.is_hitting = True
            self.__hit_cooldown = self.__hit_cd

    def __update_hitting(self, delta_time):
        self.hit_rect.center = self.position.xy + self._render_offset
        if not self.is_hitting:
            return

        if self.__hit_dir == "right":
            self.hit_rect.left = self.rect.right
        elif self.__hit_dir == "left":
            self.hit_rect.right = self.rect.left

        self.__hit_cooldown -= delta_time
        if self.__hit_cooldown <= 0:
            self.is_hitting = False
            self.hit_rect.w = 0
            self.hit_rect.h = 0
