import pygame
from dinos.common.game_abstract import Renderable
from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.environment.platform import Platform
from dinos.resources.asset_manager import AssetManager


class GamePlayEnvironment(Renderable):

    def __init__(self):
        self.__platforms = RenderGroup()

    def enter(self):
        self.__background = AssetManager.instance().image.get(
            Config.get("game_play", "environment", "background", "image")
        )
        self.__platforms.add(Platform(
            Config.get("game_play", "environment", "ground", "position"),
            Config.get("game_play", "environment", "ground", "tiles_width")
        ))

    def render(self, surface):
        surface.blit(self.__background, (0, 0))
        self.__platforms.render(surface)

    def quit(self):
        self.__platforms.empty()

    def check_ground_sprite(self, sprite):
        for platform in pygame.sprite.spritecollide(sprite, self.__platforms, False):
            is_touching = self.__check_ground(sprite, platform)
            if is_touching:
                break

    def check_ground_spritegroup(self, spritegroup):
        for sprite, platforms in pygame.sprite.groupcollide(spritegroup, self.__platforms, False, False).items():
            for platform in platforms:
                is_touching = self.__check_ground(sprite, platform)
                if is_touching:
                    break

    def __check_ground(self, sprite, platform):
        prev_feet = sprite.prev_rect.bottom
        feet = sprite.rect.bottom
        if (
            (feet >= platform.rect.top and feet <= platform.rect.bottom)
            or (feet >= platform.rect.bottom and prev_feet <= platform.rect.top)
        ):
            sprite.is_touching_ground()
            return True
        return False
