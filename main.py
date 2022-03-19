from Controller import Controller
Controller()

"""
4 Gewinnt spielweise:

"""
"""

|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
 ____ ____ ____ ____ ____ ____ ____
 
 
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    | >< |    |    |
|    |    |    | >< | () |    |    |
|    |    | >< | () | >< |    |    |
|    | >< | () | () | () |    |    |
 ____ ____ ____ ____ ____ ____ ____
-> earliest turn to win as player 2 diagonally: 10

|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    | [] |    | <> |    |    |    |
|    | [] |    | <> |    |    |    |
|    | <> | [] | <> |    | <> |    |
|    | [] | <> | [] | <> | [] |    |
 ____ ____ ____ ____ ____ ____ ____
 
 
|    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |
|    |    |    |    | () |    |    |
|    |    |    | () | >< |    |    |
|    |    | () | >< | >< |    |    |
|    | () | >< | >< | () | () |    |
 ____ ____ ____ ____ ____ ____ ____
-> earliest turn to win as player 1 diagonally: 11

Store:
 
 1 2 3 4 5 6 7
| | | | | | | | 6
| | | | | | | | 5 
| | | | | | | | 4 
| | | | | | | | 3
| | | | | | | | 2
| | | | | | | | 1
 - - - - - - -


pattern = "ahahaa"
    last = { 
      "h" : 3,
      "a" : 5
    }
text = "aslaaadahaahahaa"
           |
           j points here (j = 3) (and so does the i)
           while k = 5 (or k+1 = 6)
           j makes i shift by 6-3 ( m - j )
           k would shift i by 6-6 ( m - k+1 ) - and essentially halt the algorithm
           however, would j point towards a letter that does not exist in the dictionary,
           i would shift by an entire patternlength as k = 0 ( -1 + 1). speeding up the algorithm,
           as j could have a value of 5 which would shift the index by only 1 character...


"""

"""

# a longer more redundant way of checking diagonals without more nested loops (same efficiency)
length = 1
x, y = i + 1, j + 1
while (playboard.playingfield[x][y] and
       (playboard.playingfield[x][y] == symbol_to_look_for)):
    visited_symbols.append((x, y))
    x, y = x + 1, y + 1
    length += 1

x, y = i - 1, j - 1
while (playboard.playingfield[x][y] and
       (playboard.playingfield[x][y] == symbol_to_look_for)):
    visited_symbols.append((x, y))
    x, y = x - 1, y - 1
    length += 1

if length > 3:
    return True

# check top left to bottom right first
length = 1
x, y = i - 1, j + 1
while (playboard.playingfield[x][y] and
       (playboard.playingfield[x][y] == symbol_to_look_for)):
    visited_symbols.append((x, y))
    x, y = x - 1, y + 1
    length += 1

x, y = i + 1, j - 1
while (playboard.playingfield[x][y] and
       (playboard.playingfield[x][y] == symbol_to_look_for)):
    visited_symbols.append((x, y))
    x, y = x + 1, y - 1
    length += 1

if length > 3:
    return True
"""


