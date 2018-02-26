from fancy_print import FancyPrint


class GUI:
    def __init__(self):
        # for better visualization, an instance of "FancyPrint" is needed
        self.__fancy_print = FancyPrint()

    def show(self, board, width, height, id_to_symbol, winning_line=False):
        # firstly, print column names (usually from 1 to 7)
        print(' ' + ' '.join(map(str, range(1, width + 1))))
        # if a player has won, highlight the winning line
        if winning_line:
            # because (0, 0) is the bottom-left corner of board, y has to iterate backwards through rows
            for y in range(height - 1, -1, -1):
                # output left barrier
                print(end="|")
                # print player symbols instead of player id (unoccupied fields are represented as spaces) for each field
                # columns are separated using the pipe symbol
                for x in range(width):
                    if (x, y) in winning_line:
                        # highlight the symbol on this field to show the winning line
                        self.__fancy_print.yellow(id_to_symbol[board[(x, y)]], '|')
                    else:
                        # a standard field is printed with default font style
                        print(id_to_symbol[board[(x, y)]], end="|")
                # print a line break so that next row starts in the next line
                print()
        else:
            # because (0, 0) is the bottom-left corner of board, y has to iterate backwards through rows
            for y in range(height - 1, -1, -1):
                # output left barrier
                print(end="|")
                # print player symbols instead of player id (unoccupied fields are represented as spaces) for each field
                # columns are separated using the pipe symbol
                for x in range(width):
                    print(id_to_symbol[board[(x, y)]], end="|")
                # print a line break so that next row starts in the next line
                print()
