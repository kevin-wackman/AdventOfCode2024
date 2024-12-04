from filehandling import open_data_file_as_lines
import re

DATA_FILE = "day3in.txt"
DO = "do()"
DONT = "don't()"

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    total = 0
    wholelines = "".join(lines)
    for line in lines:
        total += get_line_sum(line)
    print(total)
    print(get_sum_do_dont(wholelines))

def get_line_sum(line):
    if not line:
        return 0
    # regex lovingly taken from chat GPT
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, line)
    total = 0
    for match in matches:
        total += (int(match[0]) * int(match[1]))
    return total

def get_sum_do_dont(line):
    if not line:
        return 0
    # Split the line on the don't delimeters - the first part is enabled, and then
    # recursively run the function after filtering for a do on the other parts
    split_line = line.split(DONT, 1)
    sum = get_line_sum(split_line[0])
    if len(split_line) > 1:
        new_split = split_line[1].split(DO, 1)
        if len(new_split) > 1:
            sum += get_sum_do_dont(new_split[1])
    return sum

main()