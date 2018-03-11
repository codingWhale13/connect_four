from random import choice
from board import Board
from player import Player
from rules import Rules


class Bot(Player):
    def __init__(self, id: int, default_symbol: str) -> None:
        # set variables (without help of user)
        self.__id = id
        self.__score = 0
        # bot will always pick a random name from "NAMES" (inherited from super class "Player")
        self.__name = choice(self.NAMES)
        self.__symbol = default_symbol

    def get_move(self, board: Board, player_id: int, rules: Rules) -> int:
        # find out which moves are valid
        possible_moves = []
        for x in range(board.width):
            if rules.check_move(board.get_board(), board.height, x):
                possible_moves += [x]

        # this simple bot checks if it can win by playing a certain column first
        for x in possible_moves:
            board.do_move(x, player_id)
            if rules.check_win(board.get_board(), board.width, board.height, board.get_last_move(), player_id):
                # even though a winning move has been detected, undo it - "game" will handle further process
                board.undo_move()
                return x
            # if bot cannot win with this move, undo it
            board.undo_move()

        # if bot cannot win in this round, it checks if opponent can win and blocks his move
        opponent_player_id = 1 if player_id == 2 else 2
        for x in possible_moves:
            board.do_move(x, opponent_player_id)
            if rules.check_win(board.get_board(), board.width, board.height, board.get_last_move(),
                               opponent_player_id):
                # make sure to undo the latest move - "game" will handle further process
                board.undo_move()
                return x
            # if bot cannot prevent a win by the opponent with this move, undo it
            board.undo_move()
        # if no victory or defeat can be detected with this very limited search depth, play randomly
        return choice(possible_moves)

    # "@property" decorator makes variables accessible from outside this class even though they're private
    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def symbol(self):
        return self.__symbol

    @property
    def score(self):
        return self.__score

    # in case of a symbol collision, the symbol of a bot may be changed from outside the class
    @symbol.setter
    def symbol(self, symbol):
        self.__symbol = symbol

    # since the score needs to be updated from outside this class, it can be modified even though it's private
    @score.setter
    def score(self, score):
        self.__score = score
