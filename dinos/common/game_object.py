import pygame

from dinos.common.game_abstract import GameAbstract


class GameObject(GameAbstract, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self._position = pygame.math.Vector2(0.0, 0.0)
        self._image = pygame.Surface((0, 0))
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._render_rect = pygame.Rect(0, 0, 0, 0)

    def _center(self):
        self._rect.center = self._position.xy
        self._render_rect.center = self._position.xy
