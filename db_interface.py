import sqlite3


class DBInterface:
    # in database, each field on the board - accessible via x and y attributes - has one of these states:
    # -> 0 (empty)
    # -> 1 (occupied by player 1)
    # -> 2 (occupied by player 2)

    def __init__(self) -> None:
        # establish a connection to sqlite database and get a cursor object that operates in the context of "connection"
        self.__connection = sqlite3.connect("db.sqlite")
        self.__cursor = self.__connection.cursor()
        # make sure tables "board" and "history" exist before working with them
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS board (x INT, y INT, state INT);")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS history (x INT, y INT);")
        # delete possible leftovers from last session
        self.clear_board()
        self.clear_history()
        # "connection.commit" makes sure to execute the commands of the cursor object
        self.__connection.commit()

    def generate_board(self, width: int, height: int) -> None:
        # all current entries from table are deleted since size of board might have changed
        self.__cursor.execute("DELETE FROM board;")
        # for every (x, y) field create a new row in the table with state 0 (empty)
        for y in range(height):
            for x in range(width):
                self.__cursor.execute("INSERT INTO board (x, y, state) VALUES (?, ?, 0);", (x, y))
        self.__connection.commit()

    def get_board(self, width: int) -> dict:
        # dictionary "board" will store all fields; key is an (x, y) position and value is the state of that field
        board = {}
        # "x" and "y" mark the position of the current field
        x = 0
        y = 0
        # this command selects data in table sorted first by column "y", then by column "x"
        self.__cursor.execute("SELECT state FROM board ORDER BY y, x;")
        for element in self.__cursor.fetchall():
            board[(x, y)] = element[0]
            # if the end of a row on the board is reached, continue in the next row; if not, increase x by 1
            if x == width - 1:
                x = 0
                y += 1
            else:
                x += 1
        return board

    def clear_board(self) -> None:
        # in all entries, the state is set to zero so none of the fields are occupied anymore
        self.__cursor.execute("UPDATE board SET state = 0;")
        self.__connection.commit()

    def set_field(self, x: int, y: int, state: int) -> None:
        # the following command updates the state of the correct field (x, y) in database
        self.__cursor.execute("UPDATE board SET state = ? WHERE x = ? AND y = ?;", (state, x, y))
        self.__connection.commit()

    def get_field(self, x: int, y: int) -> int:
        # this command reads the state of field (x, y) from database
        self.__cursor.execute("SELECT state FROM board WHERE x = ? AND y = ?;", (x, y))
        # with "cursor.fetchone", the stored value of the above command can be accessed
        return self.__cursor.fetchone()[0]

    def add_to_history(self, x: int, y: int) -> None:
        # add an entry of field (x, y) into "history"
        self.__cursor.execute("INSERT INTO history (x, y) VALUES (?, ?);", (x, y))
        self.__connection.commit()

    def get_history(self) -> list:
        # return list of (x, y) moves in order they were played
        self.__cursor.execute("SELECT x, y FROM history ORDER BY rowid;")
        return self.__cursor.fetchall()

    def get_last_move(self) -> tuple:
        # this command selects only the latest entry in table "history"
        self.__cursor.execute("SELECT x, y FROM history ORDER BY rowid DESC LIMIT 1;")
        return self.__cursor.fetchone()

    def clear_history(self) -> None:
        # delete all entries from table "history"
        self.__cursor.execute("DELETE FROM history;")
        self.__connection.commit()

    def __del__(self) -> None:
        # before instance of this class is destroyed, connection to database is also closed
        self.__connection.close()
