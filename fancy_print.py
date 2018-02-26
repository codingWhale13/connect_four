class FancyPrint:
    #HEADER = '\033[95m'
    #OKBLUE = '\033[94m'
    #UNDERLINE = '\033[4m'

    def __init__(self) -> None:
        # declare needed ANSI escape sequences for colorful output to console
        self.__RED = '\033[91m'
        self.__YELLOW = '\033[93m'
        self.__BLUE = '\033[94m'
        self.__BOLD = '\033[1m'
        self.__END = '\033[0m'

    def red(self, message, line_end='\n') -> None:
        print(self.__RED + message + self.__END, end=line_end)

    def blue(self, message, line_end='\n') -> None:
        print(self.__BLUE + message + self.__END, end=line_end)

    def yellow(self, message, line_end='\n') -> None:
        print(self.__YELLOW + message + self.__END, end=line_end)  # TODO: bold?
