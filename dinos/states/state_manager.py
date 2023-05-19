
from dinos.common.listener_updatable import ListenerUpdatable
from dinos.states.game_play import GamePlay
from dinos.states.intro import Intro
from dinos.states.state_types import StateTypes


class StateManager(ListenerUpdatable):

    def __init__(self):
        self.__states = {
            StateTypes.Intro: Intro(),
            StateTypes.GamePlay: GamePlay()
        }

        self.__current_state_id = StateTypes.Intro
        self.__current_state = self.__states[self.__current_state_id]
        self.__current_state.enter()

    def handle_event(self, event):
        self.__current_state.handle_event(event)

    def update(self, delta_time):
        if self.__current_state.done:
            self.__change_state()
        self.__current_state.update(delta_time)

    def render(self, surface):
        self.__current_state.render(surface)

    def quit(self):
        self.__current_state.quit()

    def __change_state(self):
        self.__current_state.quit()

        previous_state = self.__current_state_name
        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.previous_state = previous_state

        self.__current_state.enter()
