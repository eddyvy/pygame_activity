import pygame


class SpriteSheet:

    def __init__(self, image, rows, cols):
        self.__image = image
        self.__sequences = []

        rect_width = self.__image.get_width() / cols
        rect_height = self.__image.get_height() / rows
        for row in range(rows):
            y = row * rect_height
            for col in range(cols):
                x = col * rect_width
                self.__sequences.append(pygame.Rect(
                    x, y, rect_width, rect_height))

        self.__image_flip = pygame.transform.flip(image.copy(), True, False)
        self.__sequences_flip = []
        for row in range(rows):
            y = row * rect_height
            for col in range(cols - 1, -1, -1):
                x = col * rect_width
                self.__sequences_flip.append(pygame.Rect(
                    x, y, rect_width, rect_height))

    def get_image(self, sequence, flip=False):
        if sequence >= len(self.__sequences):
            return pygame.Surface((0, 0)), pygame.Rect(0, 0, 0, 0)

        if flip:
            return self.__image_flip, self.__sequences_flip[sequence]

        return self.__image, self.__sequences[sequence]
