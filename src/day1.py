from filehandling import open_data_file_as_lines

DATA_FILE = "day1in.txt"

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    list1 = []
    list2 = []
    for line in lines:
        [val1, val2] = line.split()
        list1.append(int(val1))
        list2.append(int(val2))
    list1.sort()
    list2.sort()
    if len(list1) != len(list2):
        raise ValueError("Lists do not have the same length")
    sum = 0
    for count, val1 in enumerate(list1):
        sum += abs(val1 - list2[count])
    print(sum)

main()