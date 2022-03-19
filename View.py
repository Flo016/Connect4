class View:
    """ a bunch of functions that output to the console.
        also provides accepted inputs for questions and
        'true' inputs"""

    def __init__(self):
        """saves reoccurring questions or valid inputs"""
        self.yes_no = ["Y", "y", "YES", "YEs", "Yes", "yes", "N", "n", "NO", "No", "no"]
        self.true = ["Y", "y", "YES", "YEs", "Yes", "yes"]
        self.false = self.yes_no not in self.true
        self.lastPrintedLines = 0   # tracks how many lines have been printed since last print.
        self.save_games = []

    def load_game(self):
        self.lastPrintedLines += 1   # answer should be written in same line.
        return ["Do you want to load a previous game? [y/n]: ", self.yes_no, self.true]

    def welcome(self):
        self.lastPrintedLines += 5
        return print("Welcome to Connect 4! \n"
                     "The Game is played by typing the column \n"
                     "That you want to put your token in!\n"
                     "The first one to Connect 4 of his tokens shall be \n"
                     "the declared Winner.")

    def AI_opponent(self):
        self.lastPrintedLines += 1
        return ["Do you want to play against a bot? [y/n]: ", self.yes_no, self.true]

    def wrong_input(self):
        self.lastPrintedLines += 1
        return "wrong input, please type a valid answer: "

    """OUTDATED"""
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
            3:    ' [] '
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

        # TODO Erase previous lines

        self.lastPrintedLines = 8
        return print(rows)

    def choose_column(self):
        self.lastPrintedLines += 1
        columns = []
        for i in range(7):
            columns.append(str(i+1))
        columns.append('s')   # for saving the game.
        return ["Select a column: ", columns]

    def print_players_turn(self, player: int):
        self.lastPrintedLines += 1
        return print("Player " + str(player + 1) + ", it's your turn!")

    def print_draw(self):
        self.lastPrintedLines += 1
        return print("The Game has ended in a draw!")

    def print_winner(self, player: int):
        self.lastPrintedLines += 1
        return print("Player " + str(player + 1) + " has won the game!")

    def another_game(self):
        self.lastPrintedLines += 1
        return ["Do you want to play another game? [y/n]: ", self.yes_no, self.true]

    @staticmethod
    def print_goodbye():
        return print("See you next time!")

    def confirmation(self):
        self.lastPrintedLines += 1
        return["Are you sure? [y/n]: ", self.yes_no, self.true]

    def ask_name(self):
        self.lastPrintedLines += 1
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz0123456789"
        return["how would you like to name your SaveFile? (Alphanumeric and Space only)", letters, False]

    def show_saved_games(self):
        with open('Save_Games/SaveGame_Names.txt', 'r') as file:
            for save in (file.read()).split(';'):
                self.save_games.append(save)
                self.lastPrintedLines += 1
                print(save)

    def choose_save_game(self):
        self.lastPrintedLines += 1
        return["Which of these Save Games would you like to load? ", self.save_games]

    def AI_match(self):
        self.lastPrintedLines += 1
        return["Do you want the AI to play against another AI instead of you? [y/n]: ",
               self.yes_no, self.true]
