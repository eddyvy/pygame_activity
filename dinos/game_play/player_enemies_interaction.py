import pygame
from dinos.config import Config
from dinos.resources.sound_player import SoundPlayer


class PlayerEnemiesInteraction:

    def __init__(self, player, enemies, kill_enemy_cb):
        self.__player = player
        self.__enemies = enemies
        self.__kill_enemy = kill_enemy_cb
        self.kills = 0

        self.__player.set_shoot_action(self.__hero_shoot)
        self.__player.set_hit_action(self.__hero_hit)
        self.__last_sy = 0

    def check_player_dead(self):
        for enemy in pygame.sprite.spritecollide(self.__player, self.__enemies, False):
            if enemy.is_dying:
                continue
            return True
        return False

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
            kills += 1

        return True

    def __hero_hit(self, hit_rect):
        SoundPlayer.instance().play_sound("whip")
        return True

    def render_debug(self, surface):
        pygame.draw.line(
            surface,
            Config.get("game", "debug", "collider_color_2"),
            (0, self.__last_sy), (Config.get(
                "game", "screen_size")[0], self.__last_sy)
        )
        pygame.draw.rect(
            surface, Config.get("game", "debug", "collider_color_2"),
            self.__player.hit_rect,
            1
        )
