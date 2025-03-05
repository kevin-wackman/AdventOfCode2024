from filehandling import open_data_file_as_lines
from functools import cache

DATA_FILE = "day19in.txt"

TEST_TOWELS = ("r", "wr", "b", "g", "bwu", "rb", "gb", "br")
TEST_DESIGNS = [
    "brwrr",
    "bggr",
    "gbbr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]

@cache
def is_valid_design(towels, design):
    if design == "":
        return 1
    total = 0
    for towel in towels:
        if design.startswith(towel):
            total += is_valid_design(towels, design[len(towel):])
    return total

def process_input(lines):
    towels = tuple(word for word in lines[0].strip().split(', '))
    designs = [line.strip() for line in lines[2:]]
    return (towels, designs)

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    (towels, designs) = process_input(lines)
    total_valid_designs = 0
    for design in designs:
        total_valid_designs += is_valid_design(towels, design)
    print(total_valid_designs)

main()