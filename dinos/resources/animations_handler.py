from dinos.common.game_abstract import Renderable, Updatable
from dinos.config import Config
from dinos.resources.animation import Animation
from dinos.resources.asset_manager import AssetManager


class AnimationsHandler(Updatable):
    def __init__(self, animations_name, initial_animation):
        self.__animations_data = Config.get(
            "animations", animations_name, "animations")
        self.__spritesheet_name = Config.get(
            "animations", animations_name, "spritesheet")
        self.__spritesheet = AssetManager.instance(
        ).spritesheet.get(self.__spritesheet_name)

        self.__animations = {}
        self.__reverse = {}
        for animation_name in list(self.__animations_data.keys()):
            data = self.__animations_data[animation_name]

            if "reverse" in data:
                self.__reverse[animation_name] = data["reverse"]
                continue

            self.__animations[animation_name] = Animation(
                data["sequence"], data["duration"]
            )

        self.__set_current_animation(initial_animation)

        self.__backup_animation_name = initial_animation
        self.__running_once = False

    def update(self, delta_time):
        if self.__running_once:
            prev_frame = self.__current_animation.get_current_frame()
            self.__current_animation.update(delta_time)
            new_frame = self.__current_animation.get_current_frame()

            if new_frame < prev_frame:
                self.__running_once = False
                self.__set_current_animation(self.__backup_animation_name)
            else:
                return

        self.__current_animation.update(delta_time)

    def quit(self):
        pass

    def animate(self, name):
        self.__backup_animation_name = name
        if self.__current_animation_name == name or self.__running_once:
            return

        self.__set_current_animation(name)
        self.__current_animation.restart()

    def animate_once(self, name):
        if self.__current_animation_name == name or self.__running_once:
            return

        self.__running_once = True
        self.__set_current_animation(name)
        self.__current_animation.restart()

    def get_current_animation(self):
        return self.__current_animation

    def get_current_animation_name(self):
        return self.__current_animation_name

    def get_current_image(self):
        return self.__spritesheet.get_image(
            self.__current_animation.get_current_spritesheet_seq(),
            self.__current_reversed
        )

    def __set_current_animation(self, name):
        self.__current_animation_name = name
        if name in self.__reverse:
            self.__current_animation = self.__animations[self.__reverse[name]]
            self.__current_reversed = True
        else:
            self.__current_animation = self.__animations[name]
            self.__current_reversed = False
