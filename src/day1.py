from filehandling import open_data_file_as_lines
from collections import Counter

DATA_FILE = "day1in.txt"

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    list1 = []
    list2 = []
    for line in lines:
        [val1, val2] = line.split()
        list1.append(int(val1))
        list2.append(int(val2))

    # Part 1 solution    
    sorted1 = sorted(list1)
    sorted2 = sorted(list2)
    if len(list1) != len(list2):
        raise ValueError("Lists do not have the same length")
    sum = 0
    for count, val1 in enumerate(sorted1):
        sum += abs(val1 - sorted2[count])
    print(sum)

    # Part 2 solution
    counts2 = Counter(list2)
    similarity = 0
    for val1 in list1:
        similarity += val1 * counts2[val1]
    print(similarity)


main()