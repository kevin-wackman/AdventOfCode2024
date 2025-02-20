from filehandling import open_data_file_as_lines
from heapq import heappush, heappop
from localutils import Vector, apply_vector, get_position, rotate_clockwise, rotate_counter_clockwise, get_vector_symbol
from dataclasses import dataclass
from typing import Tuple
from copy import deepcopy

DATA_FILE = "day16in.txt"

START_SQUARE = 'S'
END_SQUARE = 'E'
WALL = '#'
UNVISITED = '.'
VISITED = '*'
VALID_MOVES = [END_SQUARE, UNVISITED]

SAMPLE_BOARD = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",  
]

# Use a priority queue to manage the movements

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, value, data):
        heappush(self.heap, (value, data))

    def pop(self):
        if self.heap:
            return heappop(self.heap)
        raise IndexError("Attempted to pop from empty queue")

    def is_empty(self):
        return len(self.heap) == 0

@dataclass(order = True)
class DirectionalPosition:
    coords: Tuple[int, int]
    direction: Vector

@dataclass(order = True)
class DirectionalPositionWithPath:
    coords: Tuple[int, int]
    direction: Vector
    path: list[Tuple[int,int]]

def find_shortest_path_value_part_1(board):
    move_queue = PriorityQueue()
    start = find_start(board)
    move_queue.push(0, start)
    while not move_queue.is_empty():
        (weight, dirpos) = move_queue.pop()
        if get_position(board, dirpos.coords) == END_SQUARE:
            return weight
        board[dirpos.coords[0]][dirpos.coords[1]] = weight
        for vec in [dirpos.direction, rotate_counter_clockwise(dirpos.direction), rotate_clockwise(dirpos.direction)]:
            new_weight = weight + 1
            if vec != dirpos.direction:
                new_weight += 1000
            new_coords = apply_vector(dirpos.coords, vec)
            new_square = get_position(board, new_coords)
            if new_square != WALL:
                if new_square in VALID_MOVES or new_square + 1000 > new_weight:
                    move_queue.push(new_weight, DirectionalPosition(new_coords, vec))
    raise ValueError("No path found for board!")

def find_shortest_path_value_part_2(board, shortest_path_value):
    move_queue = PriorityQueue()
    start = find_start(board)
    move_queue.push(0, start)
    visited_squares = set()
    while not move_queue.is_empty():
        (weight, dirpos) = move_queue.pop()
        if weight > shortest_path_value + 1200:
            continue
        if get_position(board, dirpos.coords) == END_SQUARE:
            if weight == shortest_path_value:
                visited_squares.update([dirpos.coords])
                visited_squares.update(dirpos.path)
            continue
        board[dirpos.coords[0]][dirpos.coords[1]] = weight
        was_path_touched = False
        for vec in [dirpos.direction, rotate_counter_clockwise(dirpos.direction), rotate_clockwise(dirpos.direction)]:
            new_weight = weight + 1
            if vec != dirpos.direction:
                new_weight += 1000
            new_coords = apply_vector(dirpos.coords, vec)
            new_square = get_position(board, new_coords)
            new_path = dirpos.path
            if new_square != WALL:
                if new_square in VALID_MOVES or new_square + 1001 > new_weight:
                    if not was_path_touched:
                        new_path.append(dirpos.coords)
                        was_path_touched = True
                    else:
                        new_path = deepcopy(new_path)
                    move_queue.push(new_weight, DirectionalPositionWithPath(new_coords, vec, new_path))
    return(len(visited_squares))

def find_start(board):
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square == START_SQUARE:
                return DirectionalPositionWithPath((vert, hor), Vector.RIGHT, [])

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_BOARD
    board = []
    for line in lines:
        board.append(list(line.strip()))
    board_copy = deepcopy(board)
    shortest_path_value = find_shortest_path_value_part_1(board)
    print(shortest_path_value)
    print(find_shortest_path_value_part_2(board_copy, shortest_path_value))

main()