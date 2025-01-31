from filehandling import open_data_file_as_lines
from functools import cache
from collections import defaultdict

SAMPLE_INPUT = "125 17"


DATA_FILE = "day11in.txt"

@cache
def process_stone(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        middle = len(stone_str) // 2
        return [int(stone_str[:middle]), int(stone_str[middle:])]
    return [2024 * stone]

def blink(row):
    new_row = defaultdict(int)
    for stone in row.keys():
        new_stones = process_stone(stone)
        for new_stone in new_stones:
            new_row[new_stone] += row[stone]
    return new_row

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    line = lines[0].strip()
    # line = SAMPLE_INPUT
    int_line = [int(stone) for stone in line.split(' ')]
    dict_line = defaultdict(int)
    for stone in int_line:
        dict_line[stone] += 1
    for n in range(75):
        # print("Processing line {}".format(n))
        dict_line = blink(dict_line)
    total_stones = 0
    for n in dict_line.values():
        total_stones += n
    print(total_stones)

main()