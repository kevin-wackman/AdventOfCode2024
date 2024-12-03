from filehandling import open_data_file_as_lines

DATA_FILE = "day2in.txt"

DECREASING = 0
INCREASING = 1


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    safe_lines = 0
    for line in lines:
        nums = [int(x) for x in line.split()]
        if is_line_safe(nums):
            safe_lines += 1
    print(safe_lines)



def is_line_safe(line):
    if len(line) <= 1:
        return True
    first_direction = what_step_direction(line[0], line[1])
    last = None
    for num in line:
        if last is not None:
            if first_direction != what_step_direction(last, num):
                return False
            if not is_step_safe(last, num):
                return False
        last = num
    return True

def what_step_direction(step1, step2):
    return INCREASING if (step1 < step2) else DECREASING

def is_step_safe(step1, step2):
    diff = abs(step1-step2)
    return (diff > 0 and diff <= 3)



main()    