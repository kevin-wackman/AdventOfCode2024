from filehandling import open_data_file_as_lines
from itertools import combinations
DATA_FILE = "day8in.txt"

SAMPLE_DATA = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]

EMPTY_CELL = '.'


# Approach:
# 1.) Go through the grid, store locations of each letter in a dict
# 2.) For each letter, store positions of antinodes in a dict (checking bounds)
# 3.) Count the antinodes

def get_frequency_dicts(board):
    antenna_dict = {}
    for x, row in enumerate(board):
        for y, cell in enumerate(row.strip()):
            if cell != EMPTY_CELL:
                if cell in antenna_dict.keys():
                    antenna_dict[cell].add((x,y))
                else:
                    antenna_dict[cell] = {(x,y)}
    return antenna_dict

def get_antinodes(board, antenna_dict, get_pair_antinode_func):
    max_x = len(board)
    max_y = len(board[0].strip())
    bounds = (max_x, max_y)
    antinode_set = set()
    for locs in antenna_dict.values():
        pairs = combinations(locs, 2)
        for pair in pairs:
            antinode_set.update(get_pair_antinode_func(bounds, pair[0], pair[1]))
    return antinode_set


def get_pair_antinodes(bounds, loc1, loc2):
    antinodes = []
    x_delta = loc2[0] - loc1[0]
    y_delta = loc2[1] - loc1[1]
    antinodes.append((loc1[0] - x_delta, loc1[1] - y_delta))
    antinodes.append((loc2[0] + x_delta, loc2[1] + y_delta))
    return [antinode for antinode in antinodes if is_in_bounds(bounds, antinode)]

def get_pair_antinodes_part_2(bounds, loc1, loc2):
    antinodes = []
    x_delta = loc2[0] - loc1[0]
    y_delta = loc2[1] - loc1[1]
    current_loc = loc1
    while is_in_bounds(bounds, current_loc):
        antinodes.append(current_loc)
        current_loc = (current_loc[0] - x_delta, current_loc[1] - y_delta)
    current_loc = loc2
    while is_in_bounds(bounds, current_loc):
        antinodes.append(current_loc)
        current_loc = (current_loc[0] + x_delta, current_loc[1] + y_delta)
    return antinodes


def is_in_bounds(bounds, loc):
    (max_x, max_y) = bounds
    (x, y) = loc
    if (x < 0 or x >= max_x):
        return False
    return (y >= 0 and y < max_y)

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_DATA
    frequency_dict = get_frequency_dicts(lines)
    antinode_set = get_antinodes(lines, frequency_dict, get_pair_antinodes)
    print(len(antinode_set))
    second_antinode_set = get_antinodes(lines, frequency_dict, get_pair_antinodes_part_2)
    print(len(second_antinode_set))

main()