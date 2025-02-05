from filehandling import open_data_file_as_lines
from localutils import Vector, get_neighbors, string_to_digits, is_in_bounds, get_position
from collections import deque

DATA_FILE = "day10in.txt"
START = 0
SUMMIT = 9
SAMPLE_INPUT = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]

def trailhead_summits(map, coords):
    # use BFS to find all valid summits
    paths = deque()
    summits = set()
    paths.append(coords)
    while paths:
        position = paths.popleft()
        for neighbor in get_neighbors(position):
            if (not is_in_bounds(map, neighbor)) or (not is_gentle_slope(map, position, neighbor)):
                continue
            if get_position(map, neighbor) == SUMMIT:
                summits.add(neighbor)
            else: # Don't continue walking if it's a summit
                paths.append(neighbor)
    return summits

def trailhead_paths(map, coords):
    # Use DFS to find all paths, don't need to track previous positions since we're going 
    summit_paths = 0
    for neighbor in get_neighbors(coords):
        if (not is_in_bounds(map, neighbor)) or (not is_gentle_slope(map, coords, neighbor)):
            continue
        if get_position(map, neighbor) == SUMMIT:
            summit_paths += 1
        else:
            summit_paths += trailhead_paths(map, neighbor)
    return summit_paths

def is_gentle_slope(map, start, neighbor):
    return get_position(map, neighbor) - get_position(map, start) == 1

def get_starting_positions(map):
    starts = set()
    for x, row in enumerate(map):
        for y, value in enumerate(row):
            if value == START:
                starts.add((x,y))
    return starts

def solve_part_1(map):
    total_summits = 0
    trailheads = get_starting_positions(map)
    for trailhead in trailheads:
        total_summits += len(trailhead_summits(map, trailhead))
    return total_summits

def solve_part_2(map):
    total_paths = 0
    trailheads = get_starting_positions(map)
    for trailhead in trailheads:
        total_paths += trailhead_paths(map, trailhead)
    return total_paths  


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_INPUT
    map = [string_to_digits(line) for line in lines]
    print(solve_part_1(map))
    print(solve_part_2(map))

main()