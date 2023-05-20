from dinos.ui.label import UILabel


class UILabelSelectable(UILabel):

    def __init__(self, font, text, position, color, bg_color, selected_color):
        super().__init__(font, text, position, color, bg_color)
        self.__selected_color = selected_color
        self.is_selected = False
        self.__original_text = text
        self.__original_color = color

    def select(self):
        self.is_selected = True
        self.set_text('--> ' + self.__original_text)
        self.set_color(self.__selected_color)

    def unselect(self):
        self.is_selected = False
        self.set_text(self.__original_text)
        self.set_color(self.__original_color)
