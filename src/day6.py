from filehandling import open_data_file_as_lines
from enum import Enum
DATA_FILE = "day6in.txt"

UNVISITED = '.'
VISITED = 'X'
OBSTACLE = '#'
STARTING_SYMBOL = '^'

class VECTOR(Enum):
    UP = [-1,0]
    RIGHT = [0,1]
    DOWN = [1,0]
    LEFT = [0,-1]

def rotate_vector(vec):
    match vec:
        case VECTOR.UP:
            return VECTOR.RIGHT
        case VECTOR.RIGHT:
            return VECTOR.DOWN
        case VECTOR.DOWN:
            return VECTOR.LEFT
        case VECTOR.LEFT:
            return VECTOR.UP
    raise ValueError("Unexpected vector value {} found".format(vec))
    
def embark_journey(board):
    (coords, direction) = find_start(board)
    board[coords[0]][coords[1]] = VISITED
    length = 1
    while (True):
        newcoords = apply_vector(coords, direction)
        if not is_in_bounds(board, newcoords):
            return length
        if board[newcoords[0]][newcoords[1]] == OBSTACLE:
            direction = rotate_vector(direction)
        else:
            coords = newcoords
            if board[coords[0]][coords[1]] == UNVISITED:
                board[coords[0]][coords[1]] = VISITED
                length += 1

def is_in_bounds(board, coords):
    if coords[0] < 0 or coords[0] >= len(board):
        return False
    if coords[1] < 0 or coords[1] >= len(board[0]):
        return False
    return True

def apply_vector(coords, vector):
    return [coords[0] + vector.value[0],
            coords[1] + vector.value[1]]

def find_start(board):
    for x, row in enumerate(board):
        for y, square in enumerate(row):
            if square == STARTING_SYMBOL:
                return ([x,y], VECTOR.UP)
    raise ValueError("No starting square found in board!")

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    board = [list(line) for line in lines]
    print(embark_journey(board))




main()