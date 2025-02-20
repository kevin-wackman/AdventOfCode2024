from filehandling import open_data_file_as_lines
from localutils import get_position, Vector, apply_vector
DATA_FILE = "day15in.txt"

TEST_BOARD = [
    "##########",
    "#..O..O.O#",
    "#......O.#",
    "#.OO..O.O#",
    "#..O@..O.#",
    "#O#..O...#",
    "#O..O..O.#",
    "#.OO.O.OO#",
    "#....O...#",
    "##########",    
]
TEST_MOVES = "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"

ROBOT = '@'
WALL = '#'
FLOOR = '.'
BOX = 'O'

def get_vector(char):
    match char:
        case '<':
            return Vector.LEFT
        case '^':
            return Vector.UP
        case '>':
            return Vector.RIGHT
        case 'v':
            return Vector.DOWN
    raise ValueError("Invalid movement symbol {} found".format(char))
    

def make_move(board, coords, vec):
    cur_val = '@'
    test_coords = coords
    while get_position(board, test_coords) in [ROBOT, BOX]:
        test_coords = apply_vector(test_coords, vec)
    if get_position(board, test_coords) == WALL:
        return coords
    # Move boxes
    new_robot_coords = apply_vector(coords, vec)
    # If only 1 square was moved, this will be overwritten by the next line
    board[coords[0]][coords[1]] = FLOOR
    board[test_coords[0]][test_coords[1]] = BOX
    board[new_robot_coords[0]][new_robot_coords[1]] = ROBOT
    return new_robot_coords

def score_board(board):
    sum = 0
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square == BOX:
                sum += ((100 * vert) + hor)
    return sum

def find_starting_coords(board):
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square == ROBOT:
                return (vert, hor)

def get_problem_1(board, moves):
    coords = find_starting_coords(board)
    for move in moves:
        vec = get_vector(move)
        coords = make_move(board, coords, vec)
    return score_board(board)

def read_input(lines):
    board = []
    i = 0
    while lines[i][0] == WALL:
        board.append(list(lines[i].strip()))
        i += 1
    moves = ""
    for line in lines[i:]:
        moves += line.strip()
    return (board, moves)

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    (board, moves) = read_input(lines)
    #test_board = []
    #for n in TEST_BOARD:
    #    test_board.append(list(n))
    #moves = TEST_MOVES
    print(get_problem_1(board, moves))


main()