from random import choice
from player import Player
from rules import Rules


class Bot(Player):
    def __init__(self, id: int, default_symbol: str) -> None:
        # set variables (without help of user)
        self.__id = id
        self.__score = 0
        self.__name = self.__choose_name()
        self.__symbol = default_symbol
        self.__depth = 5
        self.__rules = Rules()

    def __choose_name(self) -> str:
        # bot will always pick a random name from "NAMES" (inherited from super class "Player")
        return choice(self.NAMES)

    def __negamax(self, board, depth, alhpa, beta, multiplier) -> tuple:
        if depth == 0 or self.__rules.check_game_over(board):
            return (multiplier * score)

        best_value = -9999
        for i in range(height):
            value = -1 * negamax()
            best_value = max(best_value, value)

            alpha = max(alpha, value)
            if alhpa >= beta:
                break

        return (best_value, -1)

    def get_move(self, board) -> int:
        # "negamax" algorithm determines best move
        return self.__negamax(board, self.__depth, -999, 999, 1)[1]

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
