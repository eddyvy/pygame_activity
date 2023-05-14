from abc import abstractmethod

import pygame

from dinos.common.updatable import Updatable


class GameObject(pygame.sprite.Sprite, Updatable):

    def __init__(self):
        super().__init__()
        self.position = pygame.math.Vector2(0.0, 0.0)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.render_rect = pygame.Rect(0, 0, 0, 0)

    @abstractmethod
    def handle_event(self, event):
        pass

    def render(self, surface_dst):
        surface_dst.blit(self.image, self.render_rect, self.rect)

    def _center(self):
        self.rect.center = self.position.xy
        self.render_rect.center = self.position.xy
