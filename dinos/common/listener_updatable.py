from abc import abstractmethod

from dinos.common.updatable import Updatable


class ListenerUpdatable(Updatable):

    @abstractmethod
    def handle_event(self, event):
        pass
