from filehandling import open_data_file_as_lines
from heapq import heappush, heappop
from localutils import Vector, apply_vector, get_position, rotate_clockwise, rotate_counter_clockwise, get_vector_symbol
from dataclasses import dataclass
from typing import Tuple

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

def find_shortest_path_value(board):
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

def find_start(board):
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square == START_SQUARE:
                return DirectionalPosition((vert, hor), Vector.RIGHT)

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_BOARD
    board = []
    for line in lines:
        board.append(list(line.strip()))
    print(find_shortest_path_value(board))

main()