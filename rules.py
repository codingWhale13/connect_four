from fancy_print import FancyPrint


class Rules:
    def __init__(self) -> None:
        self.__fancy_print = FancyPrint()
        # these tuples denote changes in x and y for the 8 adjacent neighbors of any field (N, NW, W, SW, S, SE, E, NE)
        self.__x_directions = (0, 1, 1, 1, 0, -1, -1, -1)
        self.__y_directions = (1, 1, 0, -1, -1, -1, 0, 1)

    def __on_board(self, x: int, y: int, width: int, height: int) -> bool:
        # check if (x, y) is a valid position on the board
        return -1 < x < width and -1 < y < height

    def check_win(self, board: dict, width: int, height: int, last_move: tuple, player_number: int) -> bool:
        # check for at least four consecutive tokens from one player; search order is:
        # 1. vertical
        # 2. upper left - lower right
        # 3. horizontal
        # 4. lower left - upper right
        for alignment in range(4):
            # "line" stores all connected tokens that may be needed for display later
            # position of latest move will always be connected to this line, thus it's included from the beginning
            line = [last_move]
            # starting from last move's position, search for adjacent neighbors in both directions (e.g. up and down)
            for direction in range(2):
                x, y = last_move
                while True:
                    # alter "x" and "y" to get to next field; "direction" * 4 is added to original alignment in order to
                    # explore both directions of each alignment (e.g. up and down)
                    x += self.__x_directions[alignment + direction * 4]
                    y += self.__y_directions[alignment + direction * 4]
                    # check if field exists before accessing it
                    if self.__on_board(x, y, width, height):
                        if board[(x, y)] == player_number:
                            # add (x, y) position to "line" because this field belongs to player that did last move
                            line += [(x, y)]
                        else:
                            # line is interrupted - search doesn't need to be continued in this direction
                            break
                    else:
                        # if edge of board has been reached, stop searching in this direction
                        break
            # if a player has won, return the winning line
            if len(line) > 3:
                return line
        # if no win has been detected until now, return False instead of a list of tuples
        return False

    def check_game_over(self, board: dict, width: int, height: int) -> bool:
        # if all fields in the top row are occupied, the game is over
        return not all(board[(x, height - 1)] == 0 for x in range(width))

    def check_move(self, board: dict, height: int, column: int) -> bool:
        # check if there is at least one free field in desired column by looking at value of top field
        if board[(column, height - 1)] == 0:
            return True
        # let user know the move is not possible - "column" is zero-based and needs to be increased by one for display
        self.__fancy_print.fail("Column {} is already full! Try again.".format(column + 1))
        return False
