from abc import ABC, abstractmethod


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def quit(self):
        pass


class Updatable(ABC):
    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def quit(self):
        pass


class Renderable(ABC):
    @abstractmethod
    def render(self, surface):
        pass

    @abstractmethod
    def quit(self):
        pass


class GameAbstract(EventHandler, Updatable, Renderable):
    pass
