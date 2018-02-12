class Rules:
    def __init__(self, width=7, height=6):
        self.__width = width
        self.__height = height
        self.__board = None
        # these tuples denote changes in x and y for the 8 adjacent neighbors of any field (N, NW, W, SW, S, SE, E, NE)
        self.__x_directions = (0, 1, 1, 1, 0, -1, -1, -1)
        self.__y_directions = (1, 1, 0, -1, -1, -1, 0, 1)

    def __on_board(self, x, y):
        return -1 < x < self.__width and -1 < y < self.__height

    def check_win(self, db_connection, last_move, active_symbol):
        # check for four consecutive symbols (vertical, upper left - lower right, horizontal, lower left - upper right)
        for i in range(4):
            line = [last_move]
            for j in range(2):
                x, y = last_move
                while True:
                    x += self.__x_directions[(i + j * 4) % 8]
                    y += self.__y_directions[(i + j * 4) % 8]
                    if self.__on_board(x, y):
                        if db_connection.get_field(x, y) == active_symbol:
                            line += [(x, y)]
                        else:
                            break
                    else:
                        break

            if len(line) > 3:
                return line
        return False

    def check_game_over(self, db_interface):
        return any(db_interface.get_field(i, self.__height - 1) != 0 for i in range(self.__width))

    def is_move_possible(self, db_interface, column):
        if db_interface.get_field(column, self.__height - 1) == 0:  # check if there is at least one free field in desired column
            return True
        print("ERROR: Column " + str(column + 1) + " is already full! Try again.")
        return False
