from abc import ABC, abstractmethod


class Renderable(ABC):

    @abstractmethod
    def render(self, surface_dst):
        pass

    @abstractmethod
    def quit(self):
        pass
