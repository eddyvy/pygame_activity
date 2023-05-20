import pygame

from dinos.config import Config


class InputKeyMap():

    def __init__(self, input_keys_name):
        self.__actions_key_map = {}
        actions_keys = Config.get("input", input_keys_name)

        for action, keys in actions_keys.items():
            key_codes = []
            for k in keys:
                key_codes.append(pygame.key.key_code(k))
            self.__actions_key_map[action] = tuple(key_codes)

    def is_pressed(self, event, action_name):
        return (event.type == pygame.KEYDOWN) and (event.key in self.__actions_key_map[action_name])

    def is_released(self, event, action_name):
        return (event.type == pygame.KEYUP) and (event.key in self.__actions_key_map[action_name])
