from filehandling import open_data_file_as_lines

DATA_FILE = "day2in.txt"

DECREASING = 1
INCREASING = 2


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    safe_lines = 0
    tolerable_lines = 0
    for line in lines:
        nums = [int(x) for x in line.split()]
        if is_line_safe(nums):
            safe_lines += 1
        if is_line_tolerable(nums):
            tolerable_lines += 1
    print(safe_lines)
    print(tolerable_lines)

# Part 1
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

# Part 2
def is_line_tolerable(line):
    if is_line_safe(line):
        return True
    for idx, _ in enumerate(line):
        if is_line_safe(line[:idx] + line[idx+1:]):
            return True
    return False

def what_step_direction(step1, step2):
    return INCREASING if (step1 < step2) else DECREASING

def is_step_safe(step1, step2, direction = None):
    if direction is not None and direction != what_step_direction(step1, step2):
        return False
    diff = abs(step1-step2)
    return (diff > 0 and diff <= 3)



main()    