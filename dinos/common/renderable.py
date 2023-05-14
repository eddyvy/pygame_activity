from abc import ABC, abstractmethod

import pygame


class Renderable(ABC):

    @abstractmethod
    def render(self, surface_dst):
        pass

    @abstractmethod
    def quit(self):
        pass
