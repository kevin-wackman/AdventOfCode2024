from filehandling import open_data_file_as_lines
from functools import cache
import math
SAMPLE_INPUT = "125 17"


DATA_FILE = "day11in.txt"

def process_stone(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        middle = len(stone_str) // 2
        return [int(stone_str[:middle]), int(stone_str[middle:])]
    return [2024 * stone]

def blink(row):
    new_row = []
    for stone in row:
        new_row.extend(process_stone(stone))
    return new_row

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    line = lines[0].strip()
    # line = SAMPLE_INPUT
    int_line = [int(stone) for stone in line.split(' ')]
    for _ in range(25):
        int_line = blink(int_line)
    print(len(int_line))

main()