import pygame

from dinos.common.game_abstract import GameAbstract


class GameObject(pygame.sprite.Sprite, GameAbstract):

    def __init__(self):
        super().__init__()
        self.position = pygame.math.Vector2(0.0, 0.0)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.render_rect = pygame.Rect(0, 0, 0, 0)

    def render(self, surface):
        surface.blit(self.image, self.render_rect, self.rect)

    def _center(self):
        self.rect.center = self.position.xy
        self.render_rect.center = self.position.xy
