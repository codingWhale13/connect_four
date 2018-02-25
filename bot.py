from random import choice
from player import Player


class Bot(Player):
    def __init__(self, id):
        # set variables (without help of user)
        self.__id = id
        self.__score = 0
        self.__name = self.__choose_name()
        self.__symbol = self.__choose_symbol()
        self.__depth = 5

    def __choose_name(self):
        # bot will always pick a random name from "NAMES" (inherited from super class)
        return choice(self.NAMES)

    def __choose_symbol(self):
        # 'x' and 'o' are set as default symbols since they're well distinguishable
        return 'x' if self.__id == 1 else 'o'

    def __negamax(self, alhpa, beta, multiplier):
        if depth == 0:
            return (color * score)

        best_value = -9999
        for i in range(height):
            value = -1 * negamax()
            best_value = max(best_value, value)

            alpha = max(alpha, value)
            if alhpa >= beta:
                break

        return best_value

    def get_move(self, board):
        # "negamax"
        return self.__negamax(-999, 999, 1)[1]

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
