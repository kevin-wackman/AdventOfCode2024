from filehandling import open_data_file_as_lines
from localutils import Vector, add_tuples, string_to_digits
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
    visited = set()
    summits = set()
    paths.append(coords)
    visited.add(coords)
    while paths:
        position = paths.popleft()
        for neighbor in get_neighbors(position):
            if (not is_in_bounds(map, neighbor)) or (neighbor in visited):
                continue
            if not is_gentle_slope(map, position, neighbor):
                continue
            visited.add(neighbor)
            if get_position(map, neighbor) == SUMMIT:
                summits.add(neighbor)
            else: # Don't continue walking if it's a summit
                paths.append(neighbor)
    return summits

def is_gentle_slope(map, start, neighbor):
    return get_position(map, neighbor) - get_position(map, start) == 1

def get_starting_positions(map):
    starts = set()
    for x, row in enumerate(map):
        for y, value in enumerate(row):
            if value == START:
                starts.add((x,y))
    return starts

def get_position(map, coords):
    return map[coords[0]][coords[1]]

def is_in_bounds(map, coords):
    max_x = len(map)
    max_y = len(map[0])
    (x,y) = coords
    if (x < 0 or x >= max_x):
        return False
    return (y >= 0 and y < max_y)

def get_neighbors(coords):
    neighbors = []
    for vector in Vector:
        neighbors.append(add_tuples(coords, vector.value))
    return neighbors

def solve_part_1(map):
    total_summits = 0
    trailheads = get_starting_positions(map)
    for trailhead in trailheads:
        total_summits += len(trailhead_summits(map, trailhead))
    return total_summits



def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_INPUT
    map = [string_to_digits(line) for line in lines]
    print(solve_part_1(map))

main()