import random
from sre_parse import State

import pygame
from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.dinosaurs.dino import Dino
from dinos.dinosaurs.pool import Pool
from dinos.environment.platform import Platform

from dinos.game_play.game_play_mode import GamePlayMode
from dinos.hero.hero import Hero
from dinos.resources.asset_manager import AssetManager
from dinos.resources.sound_player import SoundPlayer
from dinos.state.state import StateTypes
from dinos.game_play.fps_stats import FPSStats


class GamePlayState(State):
    __STATE = StateTypes.GamePlay

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

        self.__last_sy = 0
        self.__platforms = RenderGroup()
        self.__enemies = RenderGroup()

    def enter(self):
        self.done = False
        self.__load_assets()
        self.__background = AssetManager.instance().image.get(
            Config.get("game_play", "background", "image"))
        self.__background = pygame.transform.scale(
            self.__background,
            (Config.get("game", "screen_size")[
             0], Config.get("game", "screen_size")[1])
        )
        self.__mode = GamePlayMode.instance()
        self.__fps_stats = FPSStats()

        self.__platforms.add(Platform(
            Config.get("game_play", "environment", "ground", "position"),
            Config.get("game_play", "environment", "ground", "tiles_width")
        ))
        self.__player = Hero(
            Config.get("game_play", "hero", "spawn_position"))
        SoundPlayer.instance().play_music_fade(Config.get("game_play", "music"))

        self.__player.set_shoot_action(self.__hero_shoot)
        self.__player.set_hit_action(self.__hero_hit)

        self.__pool = Pool(
            Config.get("game_play", "dinos", "pool_size"),
            Dino,
            self.__hero_pos
        )

    def handle_event(self, event):
        self.__mode.handle_event(event)

        if self.__mode.pause:
            return

        self.__player.handle_event(event)

    def update(self, delta_time):
        if self.__mode.debug:
            self.__fps_stats.update(delta_time)

        if self.__mode.pause:
            return

        SoundPlayer.instance().update(delta_time)

        if random.random() <= Config.get("game_play", "dinos", "spawn_prob"):
            self.__spawn_enemy()

        self.__player.update(delta_time)

        for platform in pygame.sprite.spritecollide(self.__player, self.__platforms, False):
            self.__check_ground(self.__player, platform)

        self.__enemies.update(delta_time)

        for enemy, platforms in pygame.sprite.groupcollide(self.__enemies, self.__platforms, False, False).items():
            for platform in platforms:
                self.__check_ground(enemy, platform)

        for enemy in pygame.sprite.spritecollide(self.__player, self.__enemies, False):
            # TODO kill player
            pass

    def render(self, surface):
        surface.blit(self.__background, (0, 0))

        if self.__mode.debug:
            self.__fps_stats.render(surface)
            pygame.draw.line(surface, Config.get("game", "debug", "collider_color_2"),
                             (0, self.__last_sy), (Config.get("game", "screen_size")[0], self.__last_sy))

        if self.__mode.pause:
            pass

        self.__platforms.render(surface)
        self.__player.render(surface)
        self.__enemies.render(surface)

    def quit(self):
        SoundPlayer.instance().stop_music()
        self.__player.quit()
        self.__enemies.empty()
        self.__platforms.empty()
        self.__mode.quit()
        self.__fps_stats.quit()
        self.__unload_assets()

    def __load_assets(self):
        AssetManager.instance().font.load(
            self.__STATE,
            Config.get("game_play", "fps_stats", "fps_font")
        )
        AssetManager.instance().image.load(
            self.__STATE,
            Config.get("game_play", "background", "image")
        )
        AssetManager.instance().music.load(
            self.__STATE,
            Config.get("game_play", "music")
        )
        for sfx in Config.get("game_play", "sfx"):
            AssetManager.instance().sfx.load(self.__STATE, sfx)

        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "hero", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "platform", "spritesheet")
        )
        AssetManager.instance().spritesheet.load(
            self.__STATE,
            Config.get("game_play", "dinos", "spritesheet")
        )

    def __unload_assets(self):
        AssetManager.instance().clean(StateTypes.GamePlay)

    def __check_ground(self, entity, platform):
        prev_feet = entity.prev_rect.bottom
        feet = entity.rect.bottom
        if (
            (feet >= platform.rect.top and feet <= platform.rect.bottom)
            or (feet >= platform.rect.bottom and prev_feet <= platform.rect.top)
        ):
            entity.is_touching_ground()

    def __hero_shoot(self, shoot_pos, shoot_dir):
        SoundPlayer.instance().play_sound("shoot")

        sh_x = shoot_pos[0]
        sh_y = shoot_pos[1]
        is_left = shoot_dir == "left"

        closer_enemy = None
        closer_enemy_dist = None

        self.__last_sy = sh_y

        for enemy in self.__enemies.sprites():
            on_height = sh_y >= enemy.rect.top and sh_y <= enemy.rect.bottom
            if on_height:
                enemy_dist = sh_x - enemy.position.x
                if (
                    (is_left and enemy_dist > 0) and (closer_enemy_dist == None or abs(closer_enemy_dist) > abs(enemy_dist)) or
                    ((not is_left and enemy_dist < 0) and (closer_enemy_dist ==
                     None or abs(closer_enemy_dist) > abs(enemy_dist)))
                ):
                    closer_enemy = enemy

        if closer_enemy != None:
            self.__kill_enemy(closer_enemy)

        return True

    def __hero_hit(self, hit_rect):
        SoundPlayer.instance().play_sound("whip")
        return True

    def __hero_pos(self):
        return self.__player.position

    def __spawn_enemy(self):
        enemy = self.__pool.acquire()
        if enemy != None:
            self.__enemies.add(enemy)

    def __kill_enemy(self, enemy):
        self.__enemies.remove(enemy)
        self.__pool.release(enemy)
