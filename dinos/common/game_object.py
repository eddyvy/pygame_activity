import pygame

from dinos.common.game_abstract import GameAbstract
from dinos.config import Config


class GameObject(GameAbstract, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.position = pygame.math.Vector2(0.0, 0.0)
        self._image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.render_rect = pygame.Rect(0, 0, 0, 0)
        self.prev_rect = pygame.Rect(0, 0, 0, 0)
        self._render_offset = pygame.math.Vector2(0.0, 0.0)

    def _center(self):
        self.prev_rect.center = self.rect.center
        self.rect.center = self.position.xy + self._render_offset
        self.render_rect.center = self.position.xy

    def _render_debug(self, surface):
        pygame.draw.rect(
            surface,
            Config.get("game", "debug", "render_color"),
            self.render_rect,
            1
        )
        pygame.draw.rect(
            surface, Config.get("game", "debug", "collider_color"),
            self.rect,
            1
        )
