class Board:
    def __init__(self, db_interface, width=7, height=6):
        self.__width = width
        self.__height = height
        self.__last_move = None
        db_interface.generate_board(width, height)

    def do_move(self, db_interface, column, player_number):
        # Falko's option better?
        y = 0
        while db_interface.get_field(column, y) != 0:
            y += 1
        db_interface.set_field(column, y, player_number)
        self.__last_move = (column, y)

    @property
    def last_move(self):
        return self.__last_move

    @last_move.setter
    def last_move(self, last_move):
        self.__last_move = last_move
