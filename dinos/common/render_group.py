import pygame


class RenderGroup(pygame.sprite.Group):

    def handle_event(self, event):
        for sprite in self.sprites():
            sprite.handle_event(event)

    def render(self, surface):
        for sprite in self.sprites():
            sprite.render(surface)
