from font_styles import FontStyles


class GUI:
    def __init__(self, width=7, height=6):
        self.__width = width
        self.__height = height
        self.__font_styles = FontStyles()

    def show(self, db_interface):
        print(" " + " ".join(map(str, range(1, self.__width + 1))))
        for y in range(self.__height - 1, -1, -1):
            print(end="|")
            for x in range(self.__width):
                print(db_interface.get_field(x, y), end="|")
            print()

    def show_winning_move(self, db_interface, winning_line):
        print(" 1 2 3 4 5 6 7")
        for y in range(self.__height - 1, -1, -1):
            print(end="|")
            for x in range(self.__width):
                if (x, y) in winning_line:
                    print(self.__font_styles.WARNING + self.__font_styles.BOLD + db_interface.get_field(x, y) + self.__font_styles.END, end="|")
                else:
                    print(db_interface.get_field(x, y), end="|")
            print()
