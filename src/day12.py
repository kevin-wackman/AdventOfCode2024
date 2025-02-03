from filehandling import open_data_file_as_lines
from collections import deque
from localutils import get_neighbors, is_in_bounds, get_position

DATA_FILE = "day12in.txt"

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

def find_region_stats(board, explored, start):
    members = deque()
    members.append(start)
    explored.add(start)
    symbol = get_position(board, start)
    area = 1
    perimeter = 0
    while members:
        current = members.popleft()
        for neighbor in get_neighbors(current):
            # Check if the cell is of the same type
            if not is_in_bounds(board, neighbor) or (not (get_position(board, neighbor) == symbol)):
                perimeter += 1
                continue
            if neighbor in explored:
                continue
            members.append(neighbor)
            explored.add(neighbor)
            area += 1
    return (area, perimeter)

def process_board_part_1(board):
    explored = set()
    total_price = 0
    for x, row in enumerate(board):
        for y, _ in enumerate(row):
            if (x,y) not in explored:
                (area, perimeter) = find_region_stats(board, explored, (x,y))
                # print("A region of {} plants with price {} * {} = {}".format(
                #     get_position(board, (x,y)), area, perimeter, area*perimeter))
                total_price += area * perimeter
    return total_price

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    board = [line.strip() for line in lines]
    # board = SAMPLE_INPUT
    print(process_board_part_1(board))

main()