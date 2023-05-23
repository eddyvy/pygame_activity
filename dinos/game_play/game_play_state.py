import random
from sre_parse import State

from dinos.common.render_group import RenderGroup
from dinos.config import Config
from dinos.dinosaurs.dino import Dino
from dinos.dinosaurs.pool import Pool
from dinos.game_play.fps_stats import FPSStats
from dinos.game_play.game_play_assets_loader import GamePlayAssetsLoader
from dinos.game_play.game_play_environment import GamePlayEnvironment
from dinos.game_play.game_play_mode import GamePlayMode
from dinos.game_play.player_enemies_interaction import PlayerEnemiesInteraction
from dinos.hero.hero import Hero
from dinos.resources.sound_player import SoundPlayer
from dinos.state.state import StateTypes


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

        self.__pool = Pool(
            Config.get("game_play", "dinos", "pool_size"),
            Dino,
            self.__enemies_target_pos
        )

        self.__interaction = PlayerEnemiesInteraction(
            self.__player, self.__enemies, self.__kill_enemy)

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

        if self.__interaction.check_player_dead():
            # TODO kill player
            pass

    def render(self, surface):
        self.__environment.render(surface)

        if self.__mode.debug:
            self.__fps_stats.render(surface)
            self.__interaction.render_debug(surface)

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

    def __enemies_target_pos(self):
        return self.__player.position

    def __spawn_enemy(self):
        enemy = self.__pool.acquire()
        if enemy != None:
            self.__enemies.add(enemy)

    def __kill_enemy(self, enemy):
        self.__enemies.remove(enemy)
        self.__pool.release(enemy)
