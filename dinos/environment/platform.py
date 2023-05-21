import pygame
from dinos.common.game_object import GameObject
from dinos.config import Config
from dinos.game_play.game_play_mode import GamePlayMode
from dinos.resources.asset_manager import AssetManager


class Platform(GameObject):
    def __init__(self, position, tiles_width):
        super().__init__()
        self.position = pygame.math.Vector2(position)

        self.__spritesheet = AssetManager.instance().spritesheet.get(
            Config.get("game_play", "platform", "spritesheet"))

        border_left, border_left_rect = self.__spritesheet.get_image(
            Config.get("game_play", "platform", "border_left"))
        central, central_rect = self.__spritesheet.get_image(
            Config.get("game_play", "platform", "central"))
        border_right, border_right_rect = self.__spritesheet.get_image(
            Config.get("game_play", "platform", "border_right"))

        total_width = central_rect.w * tiles_width

        self._image = pygame.Surface((total_width, central_rect.h))
        self.rect = self._image.get_rect().copy()
        self.render_rect = self.rect.copy()
        infl = Config.get("game_play", "platform", "inflate_collider")
        self.rect.inflate_ip(
            self.rect.width * infl[0], self.rect.height * infl[1])
        self._render_offset = (0, 0 - (self.render_rect.h / 2))

        for tile in range(tiles_width):
            if tile == 0:
                self._image.blit(
                    border_left, (tile * border_left_rect.w, 0), border_left_rect)
            elif tile == tiles_width - 1:
                self._image.blit(
                    border_right, (tile * border_right_rect.w, 0), border_right_rect)
            else:
                self._image.blit(
                    central, (tile * central_rect.w, 0), central_rect)

        self._center()

    def handle_event(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface):
        surface.blit(self._image, self.render_rect)
        if GamePlayMode.instance().debug:
            self._render_debug(surface)

    def quit(self):
        pass
