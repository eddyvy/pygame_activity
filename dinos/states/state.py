from abc import abstractmethod
from dinos.common.game_abstract import GameAbstract


class State(GameAbstract):

    def __init__(self):
        self.done = False
        self.next_state = -1
        self.previous_state = -1

    @abstractmethod
    def enter(self):
        pass
