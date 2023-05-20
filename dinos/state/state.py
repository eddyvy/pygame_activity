from abc import abstractmethod
from enum import Enum

from dinos.common.game_abstract import GameAbstract


class StateTypes(Enum):
    Intro = 1,
    GamePlay = 2


class State(GameAbstract):

    def __init__(self):
        self.done = False
        self.next_state = -1
        self.previous_state = -1

    @abstractmethod
    def enter(self):
        pass
