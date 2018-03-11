import os
from fancy_print import FancyPrint


class GUI:
    def __init__(self) -> None:
        # for better visualization, an instance of "FancyPrint" is needed
        self.__fancy_print = FancyPrint()

    # this method simply prints the text; this makes the GUI more modular and exchangeable
    def text(self, message, line_end: str = '\n'):
        print(message, end=line_end)

    # use "fancy_print" for displaying colorful text (works only in PyCharm)
    def text_blue(self, message: str, line_end: str = '\n') -> None:
        if "PYCHARM_HOSTED" in os.environ:
            self.__fancy_print.text_blue(message, line_end)
        else:
            print(message, end=line_end)

    def text_red(self, message: str, line_end: str = '\n') -> None:
        if "PYCHARM_HOSTED" in os.environ:
            self.__fancy_print.text_red(message, line_end)
        else:
            print(message, end=line_end)

    def text_yellow(self, message: str, line_end: str = '\n') -> None:
        if "PYCHARM_HOSTED" in os.environ:
            self.__fancy_print.text_yellow(message, line_end)
        else:
            print(message, end=line_end)

    def clear_display(self):
        if "PYCHARM_HOSTED" in os.environ:
            # in PyCharm, the console is "cleared" by printing many line breaks
            print('\n' * 100)
        else:
            # depending on the operating system, different commands are executed
            os.system("cls" if os.name == "nt" else "clear")

    def show_board(self, board: dict, width: int, height: int, id_to_symbol: dict, winning_line: list = None) -> None:
        # firstly, print column names (usually from 1 to 7)
        self.text(' ' + ' '.join(map(str, range(1, width + 1))))
        # if a player has won, highlight the winning line
        if winning_line is None:
            # because (0, 0) is the bottom-left corner of board, y has to iterate backwards through rows
            for y in range(height - 1, -1, -1):
                # display left barrier
                self.text("", '|')
                # print player symbols instead of player id (unoccupied fields are represented as spaces) for each field
                # columns are separated using the pipe symbol
                for x in range(width):
                    self.text(id_to_symbol[board[(x, y)]], '|')
                # add a line break so that next row starts in next line
                self.text("")
        else:
            # because (0, 0) is the bottom-left corner of board, y has to iterate backwards through rows
            for y in range(height - 1, -1, -1):
                # display left barrier
                self.text("", '|')
                # print player symbols instead of player id (unoccupied fields are represented as spaces) for each field
                # columns are separated using the pipe symbol
                for x in range(width):
                    if (x, y) in winning_line:
                        # highlight the symbol on this field to show part of the winning line
                        self.text_yellow(id_to_symbol[board[(x, y)]], '|')
                    else:
                        # a standard field is printed with default font style
                        self.text(id_to_symbol[board[(x, y)]], '|')
                # add a line break so that next row starts in next line
                self.text("")
