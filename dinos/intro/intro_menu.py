from dinos.common.game_abstract import GameAbstract
from dinos.common.input_key_map import InputKeyMap
from dinos.config import Config
from dinos.resources.asset_manager import AssetManager
from dinos.resources.sound_player import SoundPlayer
from dinos.state.state import StateTypes
from dinos.ui.label import UILabel
from dinos.ui.label_selectable import UILabelSelectable


class IntroMenu(GameAbstract):

    def __init__(self, accept_cb, exit_cb):
        self.__accept_cb = accept_cb
        self.__exit_cb = exit_cb

        self.__inputs = InputKeyMap("select")

        font = AssetManager.instance().font.get(
            StateTypes.Intro,
            Config.get("intro", "font")
        )
        text = Config.get("intro", "text", Config.get("game", "language"))
        pos = Config.get("intro", "positions")
        fg_c = Config.get("game", "foreground_color")
        bg_c = Config.get("game", "background_color")
        hg_c = Config.get("intro", "highlight_color")

        self.__title = UILabel(font, text["title"], pos["title"], fg_c, bg_c)
        self.__score_text = UILabel(
            font, text["score_text"], pos["score_text"], fg_c, bg_c)
        # TODO Read best score
        self.__score = UILabel(font, "0", pos["score"], fg_c, bg_c)
        self.__start_game = UILabelSelectable(
            font, text["start"], pos["start"], fg_c, bg_c, hg_c)
        self.__exit_game = UILabelSelectable(
            font, text["exit"], pos["exit"], fg_c, bg_c, hg_c)

        self.__select_start()

        self.__option_selected = False

    def handle_event(self, event):
        if self.__inputs.is_pressed(event, "up"):
            if self.__start_game.is_selected:
                return
            self.__select_start()
            SoundPlayer.instance().play_sound(
                StateTypes.Intro, Config.get("intro", "sfx_select"))

        if self.__inputs.is_pressed(event, "down"):
            if self.__exit_game.is_selected:
                return
            self.__select_exit()
            SoundPlayer.instance().play_sound(
                StateTypes.Intro, Config.get("intro", "sfx_select"))

        if self.__inputs.is_pressed(event, "accept"):
            self.__option_selected = True

    def update(self, delta_time):
        if self.__option_selected:
            if self.__start_game.is_selected:
                self.__accept_cb()
            if self.__exit_game.is_selected:
                self.__exit_cb()

    def render(self, surface):
        self.__title.render(surface)
        self.__score_text.render(surface)
        self.__score.render(surface)
        self.__start_game.render(surface)
        self.__exit_game.render(surface)

    def quit(self):
        self.__title.quit()
        self.__score_text.quit()
        self.__score.quit()
        self.__start_game.quit()
        self.__exit_game.quit()

    def __select_start(self):
        self.__start_game.select()
        self.__exit_game.unselect()

    def __select_exit(self):
        self.__start_game.unselect()
        self.__exit_game.select()
