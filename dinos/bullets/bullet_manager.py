import random

import pygame
from dinos.bullets.bullet import Bullet
from dinos.common.pool import Pool
from dinos.config import Config
from dinos.resources.sound_player import SoundPlayer


class BulletManager:

    def __init__(self, bulletsgroup):
        self.__bullets = bulletsgroup

        bullet_data = Config.get("game_play", "bullet")
        self.num = bullet_data["initial_num"]
        self.__num_outside = 0
        self.__max_num = bullet_data["max_num"]
        self.__spawn_prob = bullet_data["spawn_prob"]
        self.__spawn_area = bullet_data["spawn_area"]

        self.__pool = Pool(self.__max_num, Bullet)

    def spawn_bullet(self, from_pos):
        if (random.random() > self.__spawn_prob) or ((self.num + self.__num_outside) > self.__max_num):
            return
        self.__num_outside += 1
        bullet = self.__pool.acquire()
        if bullet == None:
            return

        SoundPlayer.instance().play_sound("new_bullet")
        self.__bullets.add(bullet)
        bullet.position = from_pos
        to_x = random.randint(self.__spawn_area["l"], self.__spawn_area["r"])
        to_y = random.randint(self.__spawn_area["t"], self.__spawn_area["b"])

        bullet.move(pygame.math.Vector2(to_x, to_y))

    def check_player_touch(self, player):
        if self.__num_outside <= 0:
            return

        for bullet in pygame.sprite.spritecollide(player, self.__bullets, False):
            self.num += 1
            self.__num_outside -= 1
            self.__bullets.remove(bullet)
            self.__pool.release(bullet)

    def quit(self):
        self.__pool.empty()
