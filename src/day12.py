from filehandling import open_data_file_as_lines
from collections import deque
from localutils import is_in_bounds, get_position, Vector, get_neighbors_with_direction, rotate_clockwise, apply_vector

DATA_FILE = "day12in.txt"
PART_1 = 0
PART_2 = 1

SAMPLE_INPUT = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]

def find_region_stats(board, explored, start, part):
    members = deque()
    members.append(start)
    explored.add(start)
    symbol = get_position(board, start)
    area = 1
    perimeter = 0
    sides = 0
    while members:
        current = members.popleft()
        for (vector, neighbor) in get_neighbors_with_direction(current):                
            if (not is_in_bounds(board, neighbor)) or (not (get_position(board, neighbor) == symbol)):
                perimeter += 1
                clockwise_direction = rotate_clockwise(vector)
                if is_symbol(board, apply_vector(neighbor, clockwise_direction), symbol) or \
                        not is_symbol(board, apply_vector(current, clockwise_direction), symbol):
                    sides += 1
                continue
            if neighbor in explored:
                continue
            members.append(neighbor)
            explored.add(neighbor)
            area += 1
    if part == PART_1:
        return (area, perimeter)
    return (area, sides)

def is_symbol(board, coords, symbol):
    if not is_in_bounds(board, coords):
        return False
    return symbol == get_position(board, coords)


def process_board(board, part):
    explored = set()
    total_price = 0
    for x, row in enumerate(board):
        for y, _ in enumerate(row):
            if (x,y) not in explored:
                (area, perimeter_or_sides) = find_region_stats(board, explored, (x,y), part)
                # print("A region of {} plants with price {} * {} = {}".format(
                #     get_position(board, (x,y)), area, perimeter, area*perimeter))
                total_price += area * perimeter_or_sides
    return total_price

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    board = [line.strip() for line in lines]
    # board = SAMPLE_INPUT
    print(process_board(board, PART_1))
    print(process_board(board, PART_2))

main()