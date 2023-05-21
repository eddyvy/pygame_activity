from dinos.common.game_abstract import Renderable, Updatable


class Animation(Updatable):
    def __init__(self, sequence, duration):
        self.__duration = duration
        self.__sequence = sequence
        self.__total_sequence = len(sequence)
        self.__current_frame = 0
        self.__last_frame_time = 0
        self.__current_sequence = sequence[0]

        if duration != None:
            self.__time_per_frame = duration / len(sequence)

    def restart(self):
        self.__current_frame = 0
        self.__last_frame_time = 0

    def update(self, delta_time):
        if self.__duration == None:
            return

        updated = False
        while self.__last_frame_time > self.__time_per_frame:
            updated = True
            self.__last_frame_time -= self.__time_per_frame
            self.__current_frame += 1
            if self.__current_frame >= self.__total_sequence:
                self.__current_frame = 0

        if updated:
            self.__current_sequence = self.__sequence[self.__current_frame]
            self.__last_frame_time = 0
        else:
            self.__last_frame_time += delta_time

    def quit(self):
        pass

    def get_current_spritesheet_seq(self):
        return self.__current_sequence

    def get_current_frame(self):
        return self.__current_frame
