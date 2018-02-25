from db_interface import DBInterface


class Board:
    def __init__(self, width=7, height=6):
        # set up relevant variables
        self.__width = width
        self.__height = height
        self.__last_move = None
        # establish a connection to sqlite database via a "DBInterface" object
        self.__db_interface = DBInterface()
        # generate a new board with given width and height by creating according entries in database
        self.__db_interface.generate_board(width, height)

    def do_move(self, column, player_number):
        # find field on which the token will "fall", starting from the bottom of the given column
        y = 0
        while self.__db_interface.get_field(column, y) != 0:
            y += 1
        # let "db_interface" update the database
        self.__db_interface.set_field(column, y, player_number)
        # save this most recent move as an (x, y) position - this makes it easier to check for a win
        self.__last_move = (column, y)

    def get_board(self):
        # simply return the dictionary requested from "db_interface"
        return self.__db_interface.get_board(self.__width, self.__height)

    def clear_board(self):
        # instruct "db_interface" to reset entries in database
        self.__db_interface.clear_board()

    # "@property" decorator makes variables accessible from outside this class even though they're private
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def last_move(self):
        return self.__last_move
