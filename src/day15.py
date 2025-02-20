from filehandling import open_data_file_as_lines
from localutils import get_position, Vector, apply_vector
from copy import deepcopy
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
BOX_LEFT = '['
BOX_RIGHT = ']'

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

def widen_char(char):
    # Python weirdness means I can't use my above named constants here.  The alternative would be define them in a class, or use an if statement.
    match char:
        case '#':
            return "##"
        case 'O':
            return "[]"
        case '.':
            return ".."
        case '@':
            return "@."
    raise ValueError("Invalid floor symbol {} found".format(char))
    

def make_move_part_1(board, coords, vec):
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

def append_if_not_present(lst, val):
    if val not in lst:
        lst.append(val)

def make_move_part_2(board, coords, vec):
    test_coords = [coords]
    is_vertical = vec in [Vector.DOWN, Vector.UP]
    test_next_move = True
    touched_coords = []
    while test_coords:
        test_next_move = False
        new_test_coords = []
        for coord in test_coords:
            touched_coords.append(coord)
            moved_coords = apply_vector(coord, vec)
            new_square = get_position(board, moved_coords)
            if new_square == WALL:
                return coords
            if new_square in [BOX_LEFT, BOX_RIGHT]:
                test_next_move = True
                append_if_not_present(new_test_coords, moved_coords)
                if is_vertical:
                    if new_square == BOX_LEFT:
                        potential_coords = apply_vector(moved_coords, Vector.RIGHT)
                        append_if_not_present(new_test_coords, potential_coords)
                    if new_square == BOX_RIGHT:
                        potential_coords = apply_vector(moved_coords, Vector.LEFT)
                        append_if_not_present(new_test_coords, potential_coords)
        test_coords = new_test_coords  
    while touched_coords:
        starting_coords = touched_coords.pop()
        square_value = get_position(board, starting_coords)
        destination_coords = apply_vector(starting_coords, vec)
        board[destination_coords[0]][destination_coords[1]] = square_value
        board[starting_coords[0]][starting_coords[1]] = FLOOR
    return apply_vector(coords, vec)

def score_board(board):
    sum = 0
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square in [BOX, BOX_LEFT]:
                sum += ((100 * vert) + hor)
    return sum

def find_starting_coords(board):
    for vert, row in enumerate(board):
        for hor, square in enumerate(row):
            if square == ROBOT:
                return (vert, hor)

def get_answer(board, moves, move_func):
    coords = find_starting_coords(board)
    for move in moves:
        vec = get_vector(move)
        coords = move_func(board, coords, vec)
    return score_board(board)


def transform_board_to_big_boxes(board):
    new_board = []
    for row in board:
        new_str = ""
        for square in row:
            new_str += widen_char(square)
        new_board.append(list(new_str))
    return new_board


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

def print_board(board):
    for row in board:
        print ("".join(row))

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    (board, moves) = read_input(lines)
    #board = []
    #for n in TEST_BOARD:
    #    board.append(list(n))
    #moves = TEST_MOVES
    new_board = transform_board_to_big_boxes(board)
    print(get_answer(board, moves, make_move_part_1))
    print(get_answer(new_board, moves, make_move_part_2))

main()