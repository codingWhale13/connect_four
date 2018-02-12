from board import Board
from bot import Bot
from db_interface import DBInterface
from gui import GUI
from player import Player
from rules import Rules


class Game:
    def __init__(self):
        self.__db_interface = DBInterface()
        self.__board = Board(self.__db_interface)
        self.__gui = GUI()
        self.__player_1 = None
        self.__player_2 = None
        self.__rules = Rules()
        self.__play()

    def __welcome(self):
        print("Ready to play CONNECT FOUR?")
        print("Here we go!\n")

    def __human_player_wanted(self, player_number):
        # let user choose type of player (human or bot)
        print("Player", player_number, "shall be")
        print("-> human (press 'H')")
        print("-> a bot (press 'B')")
        while True:
            player_type = input().lower()
            if player_type == "h":
                return True
            elif player_type == "b":
                return False
            else:
                print("Press 'H' or 'B'.")

    def __initialize_match(self):
        self.__player_1 = Player(1) if self.__human_player_wanted(1) else Bot()
        self.__player_2 = Player(2) if self.__human_player_wanted(2) else Bot()
        # ensure that players have unique names and symbols
        if self.__player_1.name == self.__player_2.name or self.__player_1.symbol == self.__player_2.symbol:
            if type(self.__player_1) == Player and type(self.__player_2) == Player:
                # if both players are human, restart initialization
                print("ERROR: Both players have the same name or symbol! Try again.")
                self.__initialize_match()
                return  # the new call of "__initialize_match()" replaces this one
            else:
                # if at least one player is a bot, resolve ambiguity automatically by creating new Bot instances
                while self.__player_1.name == self.__player_2.name or self.__player_1.symbol == self.__player_2.symbol:
                    if type(self.__player_1) == Bot:
                        self.__player_1 = Bot()
                    else:
                        self.__player_2 = Bot()

        print(end="Player 1 (")
        print(end="HUMAN") if type(self.__player_1) == Player else print(end="BOT")
        print("): " + self.__player_1.name + " is '" + self.__player_1.symbol + "'.")
        print(end="Player 2 (")
        print(end="HUMAN") if type(self.__player_2) == Player else print(end="BOT")
        print("): " + self.__player_2.name + " is '" + self.__player_2.symbol + "'.")
        print("Ready to go!\n")

    def __move(self, player):
        while True:
            desired_move = player.get_move()
            if self.__rules.is_move_possible(self.__db_interface, desired_move):
                break
        self.__board.do_move(self.__db_interface, desired_move, player.id)

    def __play_match(self):
        match_round = 0
        game_over = False
        while True:
            match_round += 1

            self.__gui.show(self.__db_interface)

            if match_round % 2 == 1:
                self.__move(self.__player_1)
                winning_line = self.__rules.check_win(self.__db_interface, self.__board.last_move, self.__player_1.symbol)
                if winning_line:
                    self.__gui.show_winning_move(self.__db_interface, winning_line)
                    print(self.__player_1.name + " has won. Good game!\n")
                    self.__player_1.score += 1
                    return
            else:
                self.__move(self.__player_2)
                winning_line = self.__rules.check_win(self.__db_interface, self.__board.last_move, self.__player_2.symbol)
                if winning_line:
                    self.__gui.show_winning_move(self.__db_interface, winning_line)
                    print(self.__player_2.name + " has won. Good game!\n")
                    self.__player_2.score += 1
                    return

            if self.__rules.check_game_over(self.__db_interface):
                self.__gui.show(self.__db_interface)
                print("It's a draw!")
                return

    def __play(self):
        self.__welcome()
        first_round = True
        while True:
            if first_round:
                self.__initialize_match()
                first_round = False
            else:
                while True:
                    input_change_player_settings = input("Do you want to change any player settings? (y/n): ").lower()
                    if input_change_player_settings == "y":
                        pass
                    if input_change_player_settings == "n":
                        print("Alright. Next match starts now!")
                        break
                    print("Press 'y' or 'n'.")

            self.__play_match()
            print("DONE!")
            break
