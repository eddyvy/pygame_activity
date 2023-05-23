import pygame
from dinos.common.game_object import GameObject
from dinos.config import Config
from dinos.game_play.game_play_mode import GamePlayMode
from dinos.resources.animations_handler import AnimationsHandler


class HeroBody(GameObject):
    def __init__(self, position):
        super().__init__()
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

    def handle_event(self, event):
        pass

    def update(self, delta_time):
        self.__update_animations(delta_time)
        self._center()

    def render(self, surface):
        image, clip = self.__animations.get_current_image()
        surface.blit(image, self.render_rect, clip)

        if GamePlayMode.instance().debug:
            self._render_debug(surface)

    def quit(self):
        self.kill()

    def __update_animations(self, delta_time):
        current_is_left = "left" in self.__animations.get_current_animation_name()
        current_is_right = "right" in self.__animations.get_current_animation_name()

        if self._is_shooting:
            if self._velocity.x < 0 or (self._velocity.x == 0 and current_is_left):
                self.__animations.animate_once("shoot_left")
            elif self._velocity.x > 0 or (self._velocity.x == 0 and current_is_right):
                self.__animations.animate_once("shoot_right")
        elif self.is_hitting:
            if self._velocity.x < 0 or (self._velocity.x == 0 and current_is_left):
                self.__animations.animate_once("hit_left")
            elif self._velocity.x > 0 or (self._velocity.x == 0 and current_is_right):
                self.__animations.animate_once("hit_right")
        elif self._velocity.x < 0:
            self.__animations.animate("walk_left")
        elif self._velocity.x > 0:
            self.__animations.animate("walk_right")
        elif self._velocity.x == 0:
            if current_is_left:
                self.__animations.animate("idle_left")
            elif current_is_right:
                self.__animations.animate("idle_right")

        self.__animations.update(delta_time)
