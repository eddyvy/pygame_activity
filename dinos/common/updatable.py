from abc import abstractmethod

from dinos.common.renderable import Renderable


class Updatable(Renderable):

    @abstractmethod
    def update(self, delta_time):
        pass
