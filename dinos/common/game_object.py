import pygame

from dinos.common.game_abstract import GameAbstract
from dinos.config import Config


class GameObject(GameAbstract, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self._position = pygame.math.Vector2(0.0, 0.0)
        self._image = pygame.Surface((0, 0))
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._render_rect = pygame.Rect(0, 0, 0, 0)
        self._render_offset = pygame.math.Vector2(0.0, 0.0)

    def _center(self):
        self._rect.center = self._position.xy + self._render_offset
        self._render_rect.center = self._position.xy

    def _render_debug(self, surface):
        pygame.draw.rect(
            surface, Config.get("game", "debug", "collider_color"),
            self._rect,
            1
        )
        pygame.draw.rect(
            surface,
            Config.get("game", "debug", "render_color"),
            self._render_rect,
            1
        )
