from board import Board
from bot import Bot
from fancy_print import FancyPrint
from gui import GUI
from player import Player
from rules import Rules


class Game:
    def __init__(self):
        # create instances of needed classes
        self.__board = Board()
        self.__gui = GUI()
        self.__rules = Rules()
        self.__fancy_print = FancyPrint()
        # player objects will be set in "initialize_match"
        self.__player_1 = None
        self.__player_2 = None
        # players will have these well distinguishable symbols by default
        self.__player_1_default_symbol = 'x'
        self.__player_2_default_symbol = 'o'
        # "id_to_symbol" translates field states from database value to output symbol; player symbols will be set later
        self.__id_to_symbol = {0: ' '}
        # start game session
        self.__play()

    def __welcome(self):
        self.__fancy_print.blue("Ready to play CONNECT FOUR?")
        self.__fancy_print.blue("Here we go!")

    def __human_player_wanted(self, player_number):
        # inform user about options
        print("Player {} shall be:".format(player_number))
        print("-> human (press 'H')")
        print("-> a bot (press 'B')")
        # ask for input until valid decision has been made
        while True:
            # let user choose type of player (human or bot) by pressing the corresponding key
            player_type = input().lower()
            if player_type == 'h':
                return True
            elif player_type == 'b':
                return False
            else:
                self.__fancy_print.red("ERROR: Press 'H' or 'B'.")

    def __initialize_match(self):
        # create either objects of "Player" or "Bot" for both players - this is decided in "human_player_wanted"
        # initialization of player names and symbols for representation on board is done in "Player" and "Bot"
        if self.__human_player_wanted(1):
            self.__player_1 = Player(1, self.__player_1_default_symbol)
        else:
            Bot(1, self.__player_1_default_symbol)
        if self.__human_player_wanted(2):
            self.__player_2 = Player(2, self.__player_2_default_symbol)
        else:
            Bot(2, self.__player_2_default_symbol)

        # ensure that players have unique names and symbols
        if self.__player_1.name == self.__player_2.name or self.__player_1.symbol == self.__player_2.symbol:
            if type(self.__player_1) == Player and type(self.__player_2) == Player:
                # if both players are human, restart initialization
                self.__fancy_print.red("ERROR: Both players have the same name or symbol! Try again.")
                self.__initialize_match()
                return  # abort current call of "initialize_match" since new one has been created
            else:
                # if at least one player is a bot, resolve ambiguity automatically
                # by creating a new Bot instance, a new random name is given
                while self.__player_1.name == self.__player_2.name:
                    if type(self.__player_1) == Bot:
                        self.__player_1 = Bot()
                    else:
                        self.__player_2 = Bot()
                # if both players have the same symbol, the human player must have chosen the default symbol that was
                # intended for the other player - to resolve this, the bot simply picks 'o' instead of 'x' or vice versa
                if type(self.__player_1) == Bot:
                    self.__player_1.symbol == self.__player_2_default_symbol
                else:
                    self.__player_2.symbol == self.__player_1_default_symbol

        # map ids to symbols
        self.__id_to_symbol[self.__player_1.id] = self.__player_1.symbol
        self.__id_to_symbol[self.__player_2.id] = self.__player_2.symbol

        # summarize player information before exiting initialization
        self.__fancy_print.blue("\nGreat. Let's start the game!")
        print("Player 1 ({}): {} is '{}'.".format("HUMAN" if type(self.__player_1) == Player else "BOT",
                                                  self.__player_1.name, self.__player_1.symbol))
        print("Player 2 ({}): {} is '{}'.\n".format("HUMAN" if type(self.__player_2) == Player else "BOT",
                                                  self.__player_2.name, self.__player_2.symbol))

    def __move(self, player):
        # a move of a bot will always be valid - thus, only for a human player further checking is needed
        if type(player) == Bot:
            self.__board.do_move(player.get_move(), player.id)
        else:
            while True:
                # "player.get_move" asks user for valid input (integer between 1 and 7)
                desired_move = player.get_move()
                # "rules.is_move_possible" checks if desired move is not against the rules
                if self.__rules.check_move(self.__board.get_board(), self.__board.height, desired_move):
                    break
            # when a legal move is given, "board.do_move" organizes actually playing it
            self.__board.do_move(desired_move, player.id)

    def __play_match(self):
        # "match_round" keeps track of number of played moves so far
        match_round = 0
        while True:
            match_round += 1
            # before asking a player what to do, show the board
            self.__gui.show(self.__board.get_board(), self.__board.width, self.__board.height, self.__id_to_symbol)
            # depending on who's turn it is, let player do a move
            if match_round % 2 == 1:
                # prompt player to do a move with method "move"
                self.__move(self.__player_1)
                # check if player 1 has won by playing the latest move
                winning_line = self.__rules.check_win(self.__board.get_board(), self.__board.width, self.__board.height,
                                                      self.__board.last_move, self.__player_1.id)
                # "winning_line" is either None or a list of tuples that store positions of tokens which led to win
                if winning_line:
                    # player 1 has won; show board (emphasizing winning line) one last time
                    self.__gui.show(self.__board.get_board(), self.__board.width, self.__board.height,
                                    self.__id_to_symbol, winning_line)
                    self.__fancy_print.blue("{} has won. Good game!".format(self.__player_1.name))
                    # increase the score of player 1 by one before exiting method
                    self.__player_1.score += 1
                    return
            else:
                # prompt player to do a move with method "move"
                self.__move(self.__player_2)
                # check if player 2 has won by playing the latest move
                winning_line = self.__rules.check_win(self.__board.get_board(), self.__board.width, self.__board.height,
                                                      self.__board.last_move, self.__player_2.id)
                # "winning_line" is either None or a list of tuples that store positions of tokens which led to win
                if winning_line:
                    # player 2 has won; show board (emphasizing winning line) one last time
                    self.__gui.show(self.__board.get_board(), self.__board.width, self.__board.height,
                                    self.__id_to_symbol, winning_line)
                    self.__fancy_print.blue("{} has won. Good game!".format(self.__player_2.name))
                    # increase the score of player 2 by one before exiting method
                    self.__player_2.score += 1
                    return

            # if board is full, show it one last time and let players know that match is a draw before exiting method
            if self.__rules.check_game_over(self.__board.get_board(), self.__board.width, self.__board.height):
                self.__gui.show(self.__board.get_board(), self.__board.width, self.__board.height, self.__id_to_symbol)
                self.__fancy_print.blue("It's a draw!")
                return

    def __settings(self):
        while True:
            input_change_player_settings = input("Do you want to change any player settings? (Y/N): ").lower()
            if input_change_player_settings == "y":
                pass  # TODO: change player settings
            if input_change_player_settings == "n":
                self.__fancy_print.blue("Alright. Next match starts now!")
                break
            self.__fancy_print.red("ERROR: Press 'Y' or 'N'.")

    def __goodbye(self):
        # self.__show_stats
        self.__fancy_print.blue("Thank you for playing. Bye for now!")

    def __keep_playing(self):
        while True:
            input_keep_playing = input("What a match! Would you like to play another one? (Y/N) ").lower()
            if input_keep_playing == 'y':
                self.__fancy_print.blue("Cool, next match starts now!")
                return True
            if input_keep_playing == 'n':
                self.__goodbye()
                return False
            self.__fancy_print.red("ERROR: Press 'Y' or 'N'.")

    def __play(self):
        # welcome players once in the beginning
        self.__welcome()
        # before playing, players need to be set etc.; this is done in "initialize_match"
        self.__initialize_match()
        # until breaking out of an infinite loop, matches are played
        while True:
            # "play_match" will carry out an entire match until a player wins or there are no moves left
            self.__play_match()
            # find out if another match is wanted and react accordingly with "keep_playing"
            if self.__keep_playing():
                self.__board.clear()
            else:
                break
