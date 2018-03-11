from db_interface import DBInterface


class Board:
    def __init__(self, width: int = 7, height: int = 6) -> None:
        # set up relevant variables
        self.__width = width
        self.__height = height
        # establish a connection to sqlite database via a "DBInterface" object
        self.__db_interface = DBInterface()
        # generate a new board with given width and height by creating according entries in database
        self.__db_interface.generate_board(width, height)

    def do_move(self, column: int, player_id: int) -> None:
        # find field on which the token will "fall", starting from the bottom of the given column
        # it is guaranteed at this point that the move is valid
        y = 0
        while self.__db_interface.get_field(column, y) != 0:
            y += 1
        # let "db_interface" update the database
        self.__db_interface.set_field(column, y, player_id)
        # save this most recent move as an (x, y) position in database - this makes it easier to check for a win
        self.__db_interface.add_to_history(column, y)

    # when a bot does a move to figure out if it's a good one, the move needs to be resettable because bot only "thinks"
    def undo_move(self) -> None:
        # find out what move needs to be reset
        undo_x, undo_y = self.__db_interface.get_last_move()
        # actually reset it
        self.__db_interface.set_field(undo_x, undo_y, 0)
        # delete the latest move from history
        self.__db_interface.clear_last_move()

    def get_board(self) -> dict:
        # simply return the dictionary requested from "db_interface"
        return self.__db_interface.get_board(self.__width)

    def clear_board(self) -> None:
        # instruct "db_interface" to reset entries in database
        self.__db_interface.clear_board()

    def get_last_move(self) -> tuple:
        # instruct "db_interface" to return the last move
        return self.__db_interface.get_last_move()

    def get_history(self) -> list:
        # instruct "db_interface" to get the entire move history as a list of tuples
        return self.__db_interface.get_history()

    def clear_history(self) -> None:
        # let "db_interface" delete game history
        self.__db_interface.clear_history()

    # "@property" decorator makes variables accessible from outside this class even though they are private
    # if width or height need to be changed by "game", new Board object must be created
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
