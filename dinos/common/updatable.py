from abc import abstractmethod

from dinos.common.renderable import Renderable


class Updatable(Renderable):

    def __init__(self):
        print('updatableee')
        super().__init__()

    @abstractmethod
    def update(self, delta_time):
        pass
