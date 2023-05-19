import pygame

from dinos.common.listener_updatable import ListenerUpdatable


class GameObject(pygame.sprite.Sprite, ListenerUpdatable):

    def __init__(self):
        super().__init__()
        self.position = pygame.math.Vector2(0.0, 0.0)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.render_rect = pygame.Rect(0, 0, 0, 0)

    def render(self, surface_dst):
        surface_dst.blit(self.image, self.render_rect, self.rect)

    def _center(self):
        self.rect.center = self.position.xy
        self.render_rect.center = self.position.xy
