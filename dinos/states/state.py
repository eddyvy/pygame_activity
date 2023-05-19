from abc import abstractmethod

from dinos.common.listener_updatable import ListenerUpdatable


class State(ListenerUpdatable):

    def __init__(self):
        self.done = False
        self.next_state = -1
        self.previous_state = -1

    @abstractmethod
    def enter(self):
        pass
