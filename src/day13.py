from filehandling import open_data_file_as_lines
from localutils import extract_ints

PART_1 = 1
PART_2 = 2
PART_2_ADDITION = 10000000000000
TOLERANCE = 0.0001

DATA_FILE = "day13in.txt"
SAMPLE_INPUT = [
"Button A: X+94, Y+34",
"Button B: X+22, Y+67",
"Prize: X=8400, Y=5400",
"",
"Button A: X+26, Y+66",
"Button B: X+67, Y+21",
"Prize: X=12748, Y=12176",
"",
"Button A: X+17, Y+86",
"Button B: X+84, Y+37",
"Prize: X=7870, Y=6450",
"",
"Button A: X+69, Y+23",
"Button B: X+27, Y+71",
"Prize: X=18641, Y=10279",
]
# Making the assumption that there's one solution per pair
# If there's not, I'll need to do a lot more math
def find_button_solution(button1, button2, prize):
    (x1, y1) = button1
    (x2, y2) = button2
    (xp, yp) = prize
    button_1_presses = (yp * x2 - xp * y2) / (x2 * y1 - y2 * x1)
    button_2_presses = (xp - x1*button_1_presses) / x2
    if is_integer(button_1_presses) and is_integer(button_2_presses):
        return round(3 * button_1_presses + button_2_presses)
    return 0

def parse_input(lines, part):
    cursor = 0
    machine_list = []
    while cursor + 2 < len(lines):
        machine = []
        current_lines = []
        for n in range(3):
            current_lines.append(lines[n+cursor])
        for n, line in enumerate(current_lines):
            numbers = extract_ints(line)
            if len(numbers) != 2:
                raise ValueError("Invalid string \"{}\" found".format(line))
            if n == 2 and part == PART_2: # If we're in the prize section for part 2, add ten trillion
                numbers[0] += PART_2_ADDITION
                numbers[1] += PART_2_ADDITION
            machine.append((numbers[0], numbers[1]))
        machine_list.append(machine)
        cursor += 4
    return machine_list

def is_integer(num):
    return TOLERANCE > abs(num - round(num))

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = SAMPLE_INPUT
    machine_list = parse_input(lines, PART_1)
    total_solution = 0
    for machine in machine_list:
        [x,y,prize] = machine
        total_solution += find_button_solution(x,y,prize)
    print(total_solution)
    machine_list = parse_input(lines, PART_2)
    total_solution = 0
    for machine in machine_list:
        [x,y,prize] = machine
        total_solution += find_button_solution(x,y,prize)
    print(total_solution)

main()