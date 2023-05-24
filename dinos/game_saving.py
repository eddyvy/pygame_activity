from importlib import resources
from os import path, getcwd
import pathlib

from dinos.config import Config


class GameSaving:

    __instance = None

    @staticmethod
    def instance():
        if GameSaving.__instance is None:
            GameSaving()
        return GameSaving.__instance

    def __init__(self):
        if not GameSaving.__instance is None:
            raise Exception("There Can Be Only One GameSaving!!!")

        GameSaving.__instance = self

        res = Config.get("game", "save_file")
        if not resources.is_resource(*res):
            current = getcwd()
            self.__save_path = path.join(current, res[0], res[1])
            self.save_score(0)
        else:
            with resources.path(*res) as file_path:
                self.__save_path = file_path

    def load_score(self):
        f = open(self.__save_path, "r")
        score = f.readline()
        f.close()
        return int(score)

    def save_score(self, score):
        f = open(self.__save_path, "w")
        f.write(str(score))
        f.close()
