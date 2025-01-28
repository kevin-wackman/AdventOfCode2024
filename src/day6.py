from filehandling import open_data_file_as_lines
from enum import Enum
from copy import deepcopy
DATA_FILE = "day6in.txt"

UNVISITED = '.'
VISITED = 'X'
OBSTACLE = '#'
STARTING_SYMBOL = '^'

VERTICAL = '|'
HORIZONTAL = '-'
INTERSECTION = '+'

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
        new_coords = apply_vector(coords, direction)
        if not is_in_bounds(board, new_coords):
            return length
        if board[new_coords[0]][new_coords[1]] == OBSTACLE:
            direction = rotate_vector(direction)
        else:
            coords = new_coords
            if board[coords[0]][coords[1]] == UNVISITED:
                board[coords[0]][coords[1]] = VISITED
                length += 1

def get_new_symbol(symbol, direction):
    if direction in [VECTOR.DOWN, VECTOR.UP]:
        if symbol == UNVISITED:
            return VERTICAL
        if symbol == HORIZONTAL:
            return INTERSECTION
    else:
        if symbol == UNVISITED:
            return HORIZONTAL
        if symbol == VERTICAL:
            return INTERSECTION
    return symbol

def check_if_in_loop(symbol, direction):
    if direction in [VECTOR.DOWN, VECTOR.UP]:
        if symbol in [VERTICAL, INTERSECTION]:
            return True
    else:
        if symbol in [HORIZONTAL, INTERSECTION]:
            return True
    return False



def find_looping_boards(board):
    (coords, direction) = find_start(board)
    board[coords[0]][coords[1]] = get_new_symbol(UNVISITED, direction)
    loops = 0
    rotations = 0
    length = 1
    while True:
        new_coords = apply_vector(coords, direction)
        if not is_in_bounds(board, new_coords):
            return loops
        if board[new_coords[0]][new_coords[1]] == OBSTACLE:
            direction = rotate_vector(direction)
            rotations += 1
        else:
            # Place an obstacle and test for a loop
            if board[new_coords[0]][new_coords[1]] == UNVISITED:
                length += 1
                new_board = deepcopy(board)
                new_board[new_coords[0]][new_coords[1]] = OBSTACLE
                if is_board_looping(new_board, coords, rotate_vector(direction)):
                    loops += 1
            if rotations == 1:
                board[coords[0]][coords[1]] = INTERSECTION
            else:
                board[coords[0]][coords[1]] = get_new_symbol(board[coords[0]][coords[1]], direction)
            rotations = 0
            coords = new_coords


def is_board_looping(board, coords, direction):
    rotations = 0
    length = 0
    while length < 10000:
        new_coords = apply_vector(coords, direction)
        if not is_in_bounds(board, new_coords):
            return False
        if board[new_coords[0]][new_coords[1]] == OBSTACLE:
            direction = rotate_vector(direction)
            rotations += 1
        else:
            length += 1
            if board[coords[0]][coords[1]] == INTERSECTION:
               if board[new_coords[0]][new_coords[1]] == get_new_symbol(UNVISITED, direction):
                    return True
            if rotations == 1:
                board[coords[0]][coords[1]] = INTERSECTION
            else:
                board[coords[0]][coords[1]] = get_new_symbol(board[coords[0]][coords[1]], direction)
            rotations = 0
            coords = new_coords   
    return True                     
    

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
    print(embark_journey(deepcopy(board)))
    print(find_looping_boards(deepcopy(board)))
    
main()