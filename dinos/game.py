import pygame

from dinos.config import Config
from dinos.resources.font_manager import FontManager
from dinos.states.state import StateTypes
from dinos.states.state_manager import StateManager


class Game:

    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(
            Config.get("game", "screen_size"), 0, 32)
        pygame.display.set_caption(Config.get("game", "title"))

        self.__running = False

        self.__load_assets()
        self.__state_manager = StateManager()

    def run(self):
        self.__running = True

        last_time = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time
            while time_since_last_update > Config.get("game", "time_per_frame"):
                time_since_last_update -= Config.get("game", "time_per_frame")

                self.__process_events()
                self.__update(Config.get("game", "time_per_frame"))

            self.__render()
        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            self.__state_manager.handle_event(event)

    def __update(self, delta_time):
        self.__state_manager.update(delta_time)

    def __render(self):
        self.__screen.fill(Config.get("game", "background_color"))
        self.__state_manager.render(self.__screen)

        pygame.display.update()

    def __quit(self):
        self.__state_manager.quit()
        pygame.quit()

    def __calc_delta_time(self, last_time):
        current = pygame.time.get_ticks()
        delta = current - last_time
        return delta, current

    def __load_assets(self):
        font_data = Config.get("fonts", "main")
        FontManager.instance().load(
            StateTypes.Global,
            font_data["name"],
            font_data["file"],
            font_data["size"]
        )

    def __unload_assets(self):
        FontManager.instance().clean(StateTypes.Global)
