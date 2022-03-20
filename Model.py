class Connect4:
    """ Creates a game of Connect 4 with functions to interact with the game"""

    def __init__(self):
        """ Builds Connect 4 Framework and stores current player"""
        self.save_files = check_saves()
        self.rows = 6
        self.columns = 7
        self.playingField = [[] for _ in range(self.columns)]
        self.players = []  # stores player objects
        self.current_player = 0
        self.tokens = 0

    class Player:
        """ Creates a Player instance with ID and a PlayerToken Symbol"""

        def __init__(self, ID: int, symbol: int, is_AI: bool):
            self.ID = ID
            self.symbol = symbol
            self.is_AI = is_AI

    def create_player(self, ID: int, symbol: int, is_AI: bool):
        self.players.append(self.Player(ID, symbol, is_AI))

    def play_turn(self, column: int) -> bool:
        """ pushes the current player symbol onto the column"""
        column -= 1
        if len(self.playingField[column]) >= self.rows:
            return False
        self.playingField[column].append(self.players[self.current_player].symbol)
        self.tokens += 1
        self.current_player = (self.current_player + 1) % 2
        return True

    def check_draw(self, tokens: int) -> bool:
        if tokens == (self.rows * self.columns):
            return True
        return False

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
            data = (file.read()).split(';')  # (6 lines for rows, 2 lines for players.)
            print(data)
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


def check_saves() -> bool:
    try:
        with open('Save_Games/SaveGame_Names.txt', 'r') as file:
            file.close()
        return True
    except FileNotFoundError:
        return False


def check_win(playBoard: Connect4) -> bool:
    symbol_to_look_for = playBoard.players[(playBoard.current_player + 1) % 2].symbol  # % players
    pattern_to_look_for = [symbol_to_look_for] * 4  # [0, 0, 0, 0]
    if playBoard.tokens < 7:  # game cannot be won before turn 7
        return False
    for column in playBoard.playingField:
        if len(column) > 3:  # check each column with > 3 tokens
            if find_boyer_moore(column, pattern_to_look_for):
                return True
    # players have to have played certain multiples of 4 tokens to win certain rows
    # min(int(play.tokens / 4), 6) because int(6*7 / 4) = 10, while only 6 rows exist.
    for i in range(min(int(playBoard.tokens / 4), 6)):
        row = []
        for j in range(playBoard.columns):
            try:
                row.append(playBoard.playingField[j][i])
            except IndexError:
                row.append(None)
        if find_boyer_moore(row, pattern_to_look_for):
            return True
    # check for diagonals
    if playBoard.tokens < 10:  # game cannot be won diagonally before turn 10
        return False
    paths = [["++", "--"], ["+-", "-+"]]

    # visit each point that has a valid symbol and walk diagonal paths with same symbol
    # don't start from already visited nodes
    visited_symbols = []
    for i in range(playBoard.columns):
        # a possible diagonal can only be a winning diagonal
        # if one point has a y coordinate of 4
        if len(playBoard.playingField[i]) < 4:
            continue
        j = 4
        if playBoard.playingField[i][j] == symbol_to_look_for:
            if check_diagonals(i, j, paths, symbol_to_look_for, playBoard):
                return True

    return False


def check_diagonals(i: int, j: int, paths: list,
                    symbol_to_look_for: str, playBoard: Connect4):
    """checks from top left to bottom right and vice versa for 4 symbols in a row"""
    for path in paths:
        length = 1
        for k in range(len(path)):
            try:
                x, y = path_traversal(i, j, path[k])
                while playBoard.playingField[x][y] == symbol_to_look_for:
                    length += 1
                    x, y = path_traversal(x, y, path[k])
            except IndexError:
                pass  # index error occurs when point (x, y) doesn't exist, so we stop
        if length > 3:
            return True
    return False


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


def find_boyer_moore(text: list, pattern: list) -> bool:
    n, m = len(text), len(pattern)
    if m == 0:
        return False  # if pattern doesnt exist

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
