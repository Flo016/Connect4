import random
from os import remove as remove_file

class Connect4:
    """ Creates a game of Connect 4 with functions to interact with the game"""

    def __init__(self):
        """ Builds Connect 4 Framework and stores current player"""
        self.save_files = self.check_update_saves()
        self.rows = 6
        self.columns = 7
        self.playingField = [[] for _ in range(self.columns)]
        self.players = []  # stores player objects
        self.current_player = 0
        self.tokens = 0
        self.best_column = None

    # player functions and class

    class Player:
        """ Creates a Player instance with ID and a PlayerToken Symbol"""

        def __init__(self, ID: int, symbol: int, is_AI: bool):
            self.ID = ID
            self.symbol = symbol
            self.is_AI = is_AI

    def create_player(self, ID: int, symbol: int, is_AI: bool):
        self.players.append(self.Player(ID, symbol, is_AI))
    
    def swap_players(self):
        self.current_player = (self.current_player + 1) % 2

    # make a turn functions:

    def play_turn(self, column: int) -> bool:
        """ pushes the current player symbol onto the column"""
        column -= 1
        if len(self.playingField[column]) >= self.rows:
            return False
        self.playingField[column].append(self.players[self.current_player].symbol)
        self.tokens += 1
        self.swap_players()
        return True

    def delete_turn(self, column: int) -> bool:
        """used for AI turn to delete the imaginary turn that was made"""
        column -= 1
        print(self.playingField)
        self.playingField[column] = self.playingField[column][:-1]
        print(self.playingField)
        self.tokens -= 1
        self.swap_players()


    def AI_make_turn(self):
        """Checks if it can win next turn, 
           if it can't it tries to deny an enemy win 
           if it can't returns random column
           i is increased by 1 because 1 is taken away at play_turn."""
        for j in range(2):
            for i in range(1,len(self.playingField)+1):
                if not self.play_turn(i):
                    continue
                print("HALLO")
                if self.check_win():
                    self.delete_turn(i)
                    if j == 1:
                        self.swap_players()
                    return i
                self.delete_turn(i)
            self.swap_players()
        return random.randrange(0, 7)

    # file management functions:

    def save_game(self, name: str):
        file_names = ""
        if self.save_files:
            with open('Save_Games/SaveGame_Names.txt', 'r') as file:
                for line in file.readlines():
                    file_names = file_names + str(line) + ';'
        file_names += name
        with open('Save_Games/SaveGame_Names.txt', 'w+') as file:
            file.write(file_names)

        with open(f'Save_Games/{name}.txt', 'w+') as file:
            String = ""
            for element in self.playingField:
                String += ';' + str(element)
            for player in self.players:
                String = String + ';' + str(player.ID) + ',' + str(player.symbol) + ',' + str(
                    player.is_AI)
            file.write(String[1:])   # delete first ';' and write

    def load_game(self, name: str) -> bool:
        """get parameters from a saved game and load them onto the Connect4 Class"""
        tokens = 0
        with open(f'Save_Games/{name}.txt', 'r') as file:
            data = (file.read()).split(';')  # (7 lines for columns, 2 lines for players.)
            for i in range(self.columns):
                tempString = data[i].strip('[]').split(', ')
                for j in range(len(tempString)):
                    if tempString[j] != '':   # skip empty columns
                        self.playingField[i].append(int(tempString[j]))
                        tokens += 1
            for i in range(self.columns - len(data), 0, 1):   # get player info with negative index
                player = data[i].split(',')
                if player[2] == 'True':
                    player[2] = True
                else:
                    player[2] = False
                self.players.append(self.Player(int(player[0]), int(player[1]), player[2]))
        self.current_player = tokens % len(self.players)
        self.tokens = tokens


    @staticmethod
    def check_update_saves() -> bool:
        # check and return if savegames exist.
        # Should savegames exist, refresh save_game list in case files got deleted.
        try:
            files_to_check = None
            with open('Save_Games/SaveGame_Names.txt', 'r') as file:
                files_to_check = file.read().split(';')
        except FileNotFoundError:
            return False
        file_names = ""
        for pot_file in files_to_check:
            try:
                with open(f'Save_Games/{pot_file}.txt', 'r') as file:
                    file_names += ';' + str(pot_file) 
            except FileNotFoundError:
                continue
        if len(file_names) == 0:
            return False
        with open('Save_Games/SaveGame_Names.txt', 'w') as file:
            file.write(file_names[1:])
        return True


    def delete_save(self, file_name):
        try:
            with open(f'Save_Games/{file_name}.txt', 'r') as file:
                file.close()
            remove_file(f'Save_Games/{file_name}.txt')
            
        except FileNotFoundError:
            pass
        self.check_update_saves()

    # end game functions:

    def check_draw(self) -> bool:
        if self.tokens == (self.rows * self.columns):
            return True
        return False
    
    def check_win(self) -> bool:
        self.swap_players()
        symbol_to_look_for = self.players[self.current_player].symbol   # get symbol from last turn
        self.swap_players()
        pattern_to_look_for = [symbol_to_look_for] * 4  # [0, 0, 0, 0]
        if self.tokens < 5:  # game cannot be won before turn 7, The AI predicts a move, so it has to start 1 turn earlier
            return False
        for column in self.playingField:
            if len(column) > 3:  # check each column with > 3 tokens
                if self.find_boyer_moore(column, pattern_to_look_for):
                    return True
        # players have to have played certain multiples of 4 tokens to win certain rows
        # min(int(play.tokens / 4), 6) because int(6*7 / 4) = 10, while only 6 rows exist.
        for i in range(min(int(self.tokens / 4), 6)):
            row = []
            for j in range(self.columns):
                try:
                    row.append(self.playingField[j][i])
                except IndexError:
                    row.append(None)
            if self.find_boyer_moore(row, pattern_to_look_for):
                return True
        # check for diagonals
        if self.tokens < 10:  # game cannot be won diagonally before turn 10
            return False
        paths = [["++", "--"], ["+-", "-+"]]
    
        # visit each point that has a valid symbol and walk diagonal paths with same symbol
        # don't start from already visited nodes
        for i in range(self.columns):
            # a possible diagonal can only be a winning diagonal
            # if one point has a y coordinate of 4
            if len(self.playingField[i]) < 4:
                continue
            j = 3
            if self.playingField[i][j] == symbol_to_look_for:
                if self.check_diagonals(i, j, paths, symbol_to_look_for):
                    return True
    
        return False

    def check_diagonals(self, i: int, j: int, paths: list,
                        symbol_to_look_for: str):
        """checks from top left to bottom right and vice versa for 4 symbols in a row"""
        for path in paths:
            length = 1
            for k in range(len(path)):
                try:
                    x, y = self.path_traversal(i, j, path[k])
                    while self.playingField[x][y] == symbol_to_look_for:
                        length += 1
                        x, y = self.path_traversal(x, y, path[k])
                except IndexError:
                    pass  # index error occurs when point (x, y) doesn't exist, so we stop
            if length > 3:
                return True
        return False

    @staticmethod
    def path_traversal(x: int, y: int, path: str) -> int:
        """Traverses a path and returns coordinates"""
    
        def add(a, b):
            a, b = a + 1, b + 1
            return a, b
    
        def sub(a, b):
            a, b = a - 1, b - 1
            if a < 0 or b < 0:
                raise IndexError
            return a, b
    
        def addSub(a, b):
            a, b = a + 1, b - 1
            if b < 0:
                raise IndexError
            return a, b
    
        def subAdd(a, b):
            a, b = a - 1, b + 1
            if a < 0:
                raise IndexError
            return a, b
    
        operators = {
            '++': add,
            '--': sub,
            '+-': addSub,
            '-+': subAdd
        }
    
        x, y = operators[path](x, y)
        return x, y

    @staticmethod
    def find_boyer_moore(text: list, pattern: list) -> bool:
        n, m = len(text), len(pattern)
        if m == 0 or m > n:
            return False  # if pattern doesnt exist or is longer than text
    
        # create dictionary  for each letter in pattern
        last = {}
        for k in range(m):
            last[pattern[k]] = k
    
        # create indexes to start from last element in pattern(j)
        # and 'possible' last element of pattern in text (i)
        i = m - 1
        j = m - 1
        while i < n:
            if text[i] == pattern[j]:
                # check if last characters match, if they do, check second last characters
                if j == 0:
                    return True  # if last characters match, pattern has been found
                else:
                    i -= 1
                    j -= 1
            # should characters not match, go len(pattern) to the right and try again.
            else:
                # essentially: k exists to to shift the index more, if letter text[i] is not in pattern
                # otherwise it is shifted by m-j. on some occasion k is lower than j even if the character is in the text, which also speeds up the algorithm a bit.
                k = last.get(text[i], -1)
                i += m - min(j, k + 1)
                j = m - 1
        return False
