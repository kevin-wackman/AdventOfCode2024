from filehandling import open_data_file_as_lines
import re

DATA_FILE = "day3in.txt"

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # regex lovingly taken from chat GPT
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    total = 0
    for line in lines:
        matches = re.findall(pattern, line)
        for match in matches:
            total += (int(match[0]) * int(match[1]))
    print(total)






main()