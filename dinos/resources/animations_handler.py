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
        for animation_name in list(self.__animations_data.keys()):
            data = self.__animations_data[animation_name]

            # TODO handle inverted animations
            if "reverse" in data:
                continue

            self.__animations[animation_name] = Animation(
                data["sequence"], data["duration"]
            )

        self.__current_animation_name = initial_animation
        self.__current_animation = self.__animations[initial_animation]

    def update(self, delta_time):
        self.__current_animation.update(delta_time)

    def quit(self):
        pass

    def animate(self, name):
        if self.__current_animation_name == name:
            return
        self.__current_animation_name = name
        self.__current_animation = self.__animations[name]
        self.__current_animation.restart()

    def get_current_animation_name(self):
        return self.__current_animation_name

    def get_current_image(self):
        return self.__spritesheet.get_image(self.__current_animation.get_current_spritesheet_seq())
