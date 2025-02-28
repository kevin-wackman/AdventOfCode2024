from filehandling import open_data_file_as_lines
from localutils import Vector, get_neighbors, is_in_bounds, get_position
from collections import deque


DATA_FILE = "day18in.txt"

SAFE = '.'
CORRUPTED = '#'
END_SQUARE = '@'
BOARD_SIZE = 71

def create_blank_board(size):
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(SAFE)
        board.append(row)
    board[size-1][size-1] = END_SQUARE
    return board

def find_shortest_path_length(board):
    coords = (0,0)
    move_count = 0
    board[coords[0]][coords[1]] = move_count
    move_queue = deque()
    move_queue.append(coords)
    while move_queue:
        move_count += 1
        new_queue = deque()
        for coords in move_queue:
            neighbors = get_neighbors(coords)
            for neighbor in neighbors:
                if is_in_bounds(board, neighbor) and get_position(board, neighbor) in [SAFE, END_SQUARE]:
                    if get_position(board, neighbor) == END_SQUARE:
                        return move_count
                    board[neighbor[0]][neighbor[1]] = move_count
                    new_queue.append(neighbor)
            move_queue = new_queue
    return -1

def corrupt_memory_location(board, coords):
    board[coords[0]][coords[1]] = CORRUPTED

def corrupt_n_squares(board, lines, n):
    for line in lines[:n]:
        int_line = line.strip().split(',')
        coords = (int(int_line[0]), int(int_line[1]))
        corrupt_memory_location(board, coords)

def clear_board(board):
    for n, row in enumerate(board):
        for m, square in enumerate(row):
            if square not in [CORRUPTED, END_SQUARE]:
                board[n][m] = SAFE
    
def find_first_blocking_square(corrupted_coords):
    board = create_blank_board(BOARD_SIZE)
    for coords in corrupted_coords:
        corrupt_memory_location(board, coords)
        if find_shortest_path_length(board) < 0:
            return coords
        clear_board(board)
    print("L")

def get_all_corrupted_coords(lines):
    coords_list = []
    for line in lines:
        if line:
            int_line = line.strip().split(',')
            coords = (int(int_line[0]), int(int_line[1]))        
            coords_list.append(coords)
    return(coords_list)

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    board = create_blank_board(BOARD_SIZE)
    corrupt_n_squares(board, lines, 1024)
    print(find_shortest_path_length(board))
    parsed_lines = get_all_corrupted_coords(lines)
    print(find_first_blocking_square(parsed_lines))

main()
