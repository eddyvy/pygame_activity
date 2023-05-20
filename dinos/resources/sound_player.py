import pygame

from dinos.config import Config
from dinos.resources.asset_manager import AssetManager


class SoundPlayer:

    __instance = None

    @staticmethod
    def instance():
        if SoundPlayer.__instance is None:
            SoundPlayer()
        return SoundPlayer.__instance

    def __init__(self):
        if not SoundPlayer.__instance is None:
            raise Exception("There Can Be Only One SoundManager!!!")

        SoundPlayer.__instance = self
        self.__sound_volume = Config.get("sound", "sfx", "volume")
        self.__music_volume = Config.get("sound", "music", "volume")

        self.__current_music = None
        self.__next_music = None

    def play_sound(self, state, name):
        sound = AssetManager.instance().sfx.get(state, name)
        sound.set_volume(self.__sound_volume)
        sound.play()

    def play_music(self, state, name):
        if name is self.__current_music:
            return

        music_filepath = AssetManager.instance().music.get(state, name)
        pygame.mixer.music.load(music_filepath)
        pygame.mixer.music.set_volume(self.__music_volume)
        self.__current_music = name
        pygame.mixer.music.play(-1)

    def stop_music(self, time=100):
        pygame.mixer.music.fadeout(time)
        self.__current_music = None

    def play_music_fade(self, state, name):
        if name is self.__current_music:
            return

        self.__next_music = state, name
        pygame.music.mixer.fadeout(Config.get("sound", "music", "fadeout"))

    def update(self, delta_time):
        if self.__next_music is None or pygame.mixer.music.get_busy():
            return

        self.play_music(self.__next_music)
        self.__current_music = self.__next_music
        self.__next_music = None
