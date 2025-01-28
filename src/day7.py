from filehandling import open_data_file_as_lines
from operator import mul, add
DATA_FILE = "day7in.txt"
SAMPLE_DATA = ["190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]

OPERATORS = [mul, add]

def concat(x, y):
    return int(str(x) + (str(y)))

OPERATORS_PART_2 = [mul, add, concat]

def get_number_of_line_solutions(total, values, operators):
    totals = [values[0]]
    for val in values[1:]:
        totals = [op(n, val) for n in totals for op in operators]
    return totals.count(total)

def parse_line(line):
    split_str = line.split(':')
    total = int(split_str[0])
    values = [int(n) for n in split_str[1].split()]
    return (total, values)


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_DATA
    passing_lines_1 = 0
    passing_lines_2 = 0
    for line in lines:
        (total, values) = parse_line(line)
        if get_number_of_line_solutions(total, values, OPERATORS) > 0:
            passing_lines_1 += total
        if get_number_of_line_solutions(total, values, OPERATORS_PART_2) > 0:
            passing_lines_2 += total
    print(passing_lines_1, passing_lines_2)

main()