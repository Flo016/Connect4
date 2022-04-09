class View:
    """ a bunch of functions that output to the console.
        also provides accepted inputs for questions and
        'true' inputs"""

    def __init__(self):
        """saves reoccurring questions or valid inputs"""
        self.yes_no = ["y", "yes", "n", "no"]
        self.true = ["y", "yes"]
        self.save_games = []
        self.welcome_string = "\n" \
                              "\n" \
                              "\n" \
                              "\n" \
                              "\n" \
                              "*************************************\n" \
                              "*             Connect 4             *\n" \
                              "*************************************\n" \
                              "*  enter 's' during a game to save! *\n"

    def load_game(self):
        return ["Do you want to load a previous game? [y/n]: ", self.yes_no, self.true]

    @staticmethod
    def welcome():
        return print("*************************************\n"
                     "*             Connect 4             *\n"
                     "*************************************\n"
                     "*  enter 's' during a game to save! *\n")

    def AI_opponent(self):
        return ["Do you want to play against a bot? [y/n]: ", self.yes_no, self.true]

    @staticmethod
    def wrong_input():
        return "wrong input, please type a valid answer: "

    def print_playingField(self, playBoard):   # takes a Connect4 Object as input.
        """ 'Build' each row individually, concatenates them,
            erases everything from last print_playingField and
            reprints playingField."""
        # fill up 'empty' slots with 'NONE'

        symbols = {
            None: '    ',
            0:    ' () ',
            1:    ' >< ',
            2:    ' <> ',
            3:    ' [] ',
            4:    ' 11 ',
        }
        rows = ""
        for i in range(playBoard.rows-1, -1, -1):   # height of a column is 6
            rows = rows + "\n|"
            for j in range(playBoard.columns):   # width of the playBoard is 7
                try:
                    rows = rows + symbols[playBoard.playingField[j][i]] + "|"
                except IndexError:
                    rows = rows + symbols[None] + "|"
        rows += "\n ____ ____ ____ ____ ____ ____ ____"
        rows += "\n   I   II  III   IV    V   VI  VII"
        return print(self.welcome_string + rows)

    @staticmethod
    def choose_column():
        columns = []
        for i in range(7):
            columns.append(str(i+1))
        columns.append('s')   # for saving the game.
        return ["Select a column: ", columns]

    @staticmethod
    def print_players_turn(player: int, is_AI: bool):
        if is_AI:
            return print("AI " + str(player + 1) + ", it's your turn!")
        return print("Player " + str(player + 1) + ", it's your turn!")

    @staticmethod
    def print_draw():
        return print("The Game has ended in a draw!")

    @staticmethod
    def print_winner(player: int, is_AI: bool):
        if is_AI:
            return print("AI " + str(player + 1) + " has won the game!")
        return print("Player " + str(player + 1) + " has won the game!")

    def another_game(self):
        return ["Do you want to play another game? [y/n]: ", self.yes_no, self.true]

    @staticmethod
    def print_goodbye():
        return print("See you next time!")

    def confirmation(self):
        return["Are you sure? [y/n]: ", self.yes_no, self.true]

    @staticmethod
    def ask_name():
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return["how would you like to name your SaveFile? (Alphanumeric Only): ", letters, False]

    def show_saved_games(self):
        self.set_saved_games()
        save_string = ""
        for save in self.save_games:
            save_string +=  str(save) + " "
        print(save_string)

    def set_saved_games(self):
        self.save_games = []   # reset array in case of repeated function calls.
        with open('Save_Games/SaveGame_Names.txt', 'r') as file:
            for save in (file.read()).split(';'):
                self.save_games.append(save)


    def load_savegame_console(self):
        return["Do you want to manage your saves? [y/n]:", self.yes_no, self.true]

    @staticmethod
    def save_game_info():
        return print("Type 'help' for a manual. Type 'ls' for a list of all savegames. ")

    def AI_match(self):
        return["Do you want the AI to play against another AI instead of you? [y/n]: ",
               self.yes_no, self.true]

    @staticmethod
    def wrong_command():
        return print("Option Error, please only use valid options and only use them once per command.")

    @staticmethod
    def wrong_filename():
        return print("This Savegame does not exist.")

    @staticmethod
    def manpage():
        return print("Type 'help' for a manual. Type 'ls' for a list of all savegames \n" \
                     "Type 'q' or 'quit' to exit the terminal\n" \
                     "\n" \
                     "*** SAVE FILE MANAGEMENT ***\n" \
                     "\n" \
                     "Syntax: FILENAME -[OPTIONS]  \n" \
                     "Options:\n" \
                     "          -l: loads a game, A game will start after you load a game!\n" \
                     "          -p: creates a preview of the savegame, showing you the playingfield.\n" \
                     "          -d: deletes the savefile.\n" \
                     "Note: Commands may be chained together in any order, i.e -lpd or -l -pd\n")
