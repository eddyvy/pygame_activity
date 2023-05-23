from dinos.common.game_abstract import Renderable


class UILabel(Renderable):

    def __init__(self, font, text, position, color, bg_color=None):
        self.__font = font
        self.__text = text
        self.__color = color
        self.__position = position
        self.__bg_color = bg_color
        self.__set_image()

    def set_text(self, text):
        if text == self.__text:
            return
        self.__text = text
        self.__set_image()

    def set_color(self, color):
        if color == self.__color:
            return
        self.__color = color
        self.__set_image()

    def set_position(self, position):
        if position == self.__position:
            return
        self.__position = position
        self.__set_image()

    def render(self, surface):
        surface.blit(self.__image, self.__rect)

    def quit(self):
        pass

    def __set_image(self):
        self.__image = self.__font.render(
            self.__text, True, self.__color, self.__bg_color)
        self.__rect = self.__image.get_rect(center=self.__position)
