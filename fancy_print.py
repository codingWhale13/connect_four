class FancyPrint:
    # declare needed ANSI escape sequences for colorful output to console
    __BLUE = '\033[94m'
    __RED = '\033[91m'
    __YELLOW = '\033[93m'
    __END = '\033[0m'

    # string "message" will be displayed in the corresponding color
    # when highlighting a single character, "line_end" can be modified so that no line break is added after the message
    def blue(self, message: str, line_end: str) -> None:
        print(type(self).__BLUE + message + type(self).__END, end=line_end)

    def red(self, message: str, line_end: str) -> None:
        print(type(self).__RED + message + type(self).__END, end=line_end)

    def yellow(self, message: str, line_end: str) -> None:
        print(type(self).__YELLOW + message + type(self).__END, end=line_end)
