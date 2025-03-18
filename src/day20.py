from filehandling import open_data_file_as_lines
from localutils import get_neighbors, is_in_bounds, get_position, get_neighbors_with_direction, apply_vector
from collections import deque, defaultdict
from copy import deepcopy
DATA_FILE = "day20in.txt"

WALL = '#'
PATH = '.'
START_SQUARE = 'S'
END_SQUARE = 'E'

SAMPLE_INPUT = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############",    
]


# Returns -1 if there is no valid path found
def find_shortest_path_length(board, coords, move_count = 0):
    board[coords[0]][coords[1]] = move_count
    move_queue = deque()
    move_queue.append(coords)
    while move_queue:
        move_count += 1
        new_queue = deque()
        for coords in move_queue:
            neighbors = get_neighbors(coords)
            for neighbor in neighbors:
                if is_in_bounds(board, neighbor) and get_position(board, neighbor) in [PATH, END_SQUARE]:
                    if get_position(board, neighbor) == END_SQUARE:
                        board[neighbor[0]][neighbor[1]] = move_count
                        return move_count
                    board[neighbor[0]][neighbor[1]] = move_count
                    new_queue.append(neighbor)
            move_queue = new_queue
    return -1

def get_starting_position(board):
    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == START_SQUARE:
                return (x,y)
    raise ValueError("No start found in board")

def find_cheat_dict(board):
    start_coords = get_starting_position(board)
    marked_board = deepcopy(board)
    cheat_dict = defaultdict(int)
    base_length = find_shortest_path_length(marked_board, start_coords)
    current_pos = start_coords
    while current_pos:
        for (vec, neighbor) in get_neighbors_with_direction(current_pos):
            if get_position(marked_board, neighbor) == WALL:
                dest_square = apply_vector(neighbor, vec)
                if is_in_bounds(marked_board, dest_square):
                    dest_val = get_position(marked_board, dest_square)
                    if dest_val != WALL:
                        cheat_diff = dest_val - (get_position(marked_board, current_pos) + 2)
                        if cheat_diff > 0:
                            cheat_dict[cheat_diff] += 1
        current_pos = get_next_square(marked_board, current_pos)
    return cheat_dict
        
# This finds the next move on a marked board
def get_next_square(board, coords):
    square_value = get_position(board, coords)
    for neighbor in get_neighbors(coords):
        neighbor_val = get_position(board, neighbor)
        if neighbor_val != WALL and neighbor_val > square_value:
            return neighbor
    return None

def how_many_cheats_at_least_threshold(cheat_dict, threshold):
    total = 0
    for (key, value) in cheat_dict.items():
        if key >= threshold:
            total += value
    return total

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_INPUT
    board = []
    for line in lines:
        board.append(list(line.strip()))
    board_copy = deepcopy(board)
    print(find_shortest_path_length(board_copy, get_starting_position(board_copy)))
    cheats = find_cheat_dict(board)
    print(how_many_cheats_at_least_threshold(cheats, 100))

main()