import sqlite3


class DBInterface:
    def __init__(self):
        self.__connection = sqlite3.connect("db.sqlite")  # establish connection
        self.__cursor = self.__connection.cursor()  # get a cursor object that operates in the context of "connection"

    def generate_board(self, width, height):
        self.__cursor.execute("DELETE FROM board")
        for y in range(height):
            for x in range(width):
                self.__cursor.execute("INSERT INTO board (x, y, color) VALUES (?, ?, 0)", (x, y))
        self.__connection.commit()

    def clear_board(self):
        self.__cursor.execute("UPDATE board SET color = 0")
        self.__connection.commit()

    def set_field(self, x: int, y: int, color: int):
        self.__cursor.execute("UPDATE board SET color = ? WHERE x = ? AND y = ?;", (color, x, y))
        self.__connection.commit()

    def get_field(self, x: int, y: int):
        self.__cursor.execute("SELECT color FROM board WHERE x = (?) AND y = (?);", (x, y))
        return self.__cursor.fetchone()[0]

    def get_board(self):
        board = [[0 for x in range(self.__width)] for y in range(self.__height)]
        for y in range(self.__height):
            self.__cursor.execute("SELECT color FROM board WHERE y = ? ORDER BY x", (str(y)))
            x = 0
            for element in self.__cursor.fetchall():
                board[y][x] = element[0]
                x += 1
        return board

    def __del__(self):
        self.__connection.close()
