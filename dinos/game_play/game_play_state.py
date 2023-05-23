import random
from sre_parse import State

import pygame
from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.dinosaurs.dino import Dino
from dinos.dinosaurs.pool import Pool
from dinos.game_play.game_play_assets_loader import GamePlayAssetsLoader
from dinos.game_play.game_play_environment import GamePlayEnvironment

from dinos.game_play.game_play_mode import GamePlayMode
from dinos.hero.hero import Hero
from dinos.resources.sound_player import SoundPlayer
from dinos.state.state import StateTypes
from dinos.game_play.fps_stats import FPSStats


class GamePlayState(State):

    def __init__(self):
        super().__init__()
        self.next_state = StateTypes.Intro

        self.__assets_loader = GamePlayAssetsLoader()
        self.__environment = GamePlayEnvironment()

        self.__last_sy = 0
        self.__enemies = RenderGroup()

    def enter(self):
        self.done = False
        self.__assets_loader.load()

        self.__mode = GamePlayMode.instance()
        self.__fps_stats = FPSStats()

        self.__environment.enter()

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
        self.__environment.check_ground_sprite(self.__player)

        self.__enemies.update(delta_time)
        self.__environment.check_ground_spritegroup(self.__enemies)

        for enemy in pygame.sprite.spritecollide(self.__player, self.__enemies, False):
            # TODO kill player
            pass

    def render(self, surface):
        self.__environment.render(surface)

        if self.__mode.debug:
            self.__fps_stats.render(surface)
            pygame.draw.line(surface, Config.get("game", "debug", "collider_color_2"),
                             (0, self.__last_sy), (Config.get("game", "screen_size")[0], self.__last_sy))

        self.__player.render(surface)
        self.__enemies.render(surface)

    def quit(self):
        SoundPlayer.instance().stop_music()
        self.__player.quit()
        self.__enemies.empty()
        self.__environment.quit()
        self.__mode.quit()
        self.__fps_stats.quit()
        self.__assets_loader.unload()

    def __hero_shoot(self, shoot_pos, shoot_dir):
        SoundPlayer.instance().play_sound("shoot")

        sh_x = shoot_pos[0]
        sh_y = shoot_pos[1]
        is_left = shoot_dir == "left"

        closer_enemy = None
        closer_enemy_dist = None

        self.__last_sy = sh_y

        for enemy in self.__enemies.sprites():
            if enemy.is_dying:
                continue

            on_height = sh_y >= enemy.rect.top and sh_y <= enemy.rect.bottom
            if on_height:
                enemy_dist = int(sh_x - enemy.position.x)
                if (
                    (is_left and enemy_dist > 0) and (closer_enemy_dist == None or closer_enemy_dist > enemy_dist) or
                    ((not is_left and enemy_dist < 0) and (closer_enemy_dist ==
                     None or closer_enemy_dist < enemy_dist))
                ):
                    closer_enemy = enemy
                    closer_enemy_dist = enemy_dist

        if closer_enemy != None:
            closer_enemy.die(self.__kill_enemy)

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
