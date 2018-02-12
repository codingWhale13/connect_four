from random import choice, randint
from player import Player


class Bot(Player):
    def __init__(self, board_width=7):
        self.__name = choice(self.NAMES)  # inherited from Player
        self.__symbol = chr(randint(33, 126))  # choose from all visible ASCII symbols
        self.__score = 0
        self.__depth = 5
        self.__board_width = board_width

    def get_move(self):
        for i in range(self.__board_width):
            pass
        return 0 # (score, move)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol):
        self.__symbol = symbol

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score
