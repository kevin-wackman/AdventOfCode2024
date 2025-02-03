from filehandling import open_data_file_as_lines
from localutils import add_tuples
from enum import Enum
from collections import defaultdict

DATA_FILE = "day14in.txt"
SAMPLE_INPUT = [
"p=0,4 v=3,-3",
"p=6,3 v=-1,-3",
"p=10,3 v=-1,2",
"p=2,0 v=2,-1",
"p=0,0 v=1,3",
"p=3,0 v=-2,-2",
"p=7,6 v=-1,-3",
"p=3,0 v=-1,-2",
"p=9,3 v=2,3",
"p=7,3 v=-1,2",
"p=2,4 v=2,-3",
"p=9,5 v=-3,-3",
]
BOARD_WIDTH = 101
BOARD_HEIGHT = 103

class Quadrant(Enum):
    NONE = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT = 4


class Robot:
    def __init__(self, position, velocity, max_width = BOARD_WIDTH, max_height = BOARD_HEIGHT):
        self.position = position
        self.velocity = velocity
        self.max_width = max_width
        self.max_height = max_height

    def cycle_n_times(self, cycles):
        total_distance = tuple([cycles * n for n in self.velocity])
        new_position = add_tuples(self.position, total_distance)
        actual_x = new_position[0] % self.max_width
        actual_y = new_position[1] % self.max_height
        self.position = (actual_x, actual_y)

    def find_quadrant(self):
        quadrant_width_check = (self.position[0] * 2) - (self.max_width - 1)
        if not quadrant_width_check:
            return Quadrant.NONE
        quadrant_height_check = (self.position[1] * 2) - (self.max_height - 1)
        if not quadrant_height_check:
            return Quadrant.NONE
        if quadrant_width_check > 0:
            if quadrant_height_check > 0:
                return Quadrant.BOTTOM_RIGHT
            return Quadrant.BOTTOM_LEFT
        if quadrant_height_check > 0:
            return Quadrant.TOP_RIGHT
        return Quadrant.TOP_LEFT


def parse_line(line, max_width = BOARD_WIDTH, max_height = BOARD_HEIGHT):
    pv_array = line.strip().split(' ')
    parts = []
    for part in pv_array:
        nums = part.split('=')[1].split(',')
        parts.append((int(nums[0]), int(nums[1])))
    return Robot(parts[0], parts[1], max_width, max_height)


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    #lines = SAMPLE_INPUT
    sample_max_width = 11
    sample_max_height = 7
    cycles = 100
    robots = []
    quadrant_count = defaultdict(int)
    for line in lines:
        robots.append(parse_line(line))
        # robots.append(parse_line(line, sample_max_width, sample_max_height))
    for robot in robots:
        robot.cycle_n_times(cycles)
        quadrant = robot.find_quadrant()
        quadrant_count[quadrant] += 1
    quadrant_count[Quadrant.NONE] = 1
    total = 1
    for robot_counts in quadrant_count.values():
        total *= robot_counts
    print(total)

main()