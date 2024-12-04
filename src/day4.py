from filehandling import open_data_file_as_lines

DIRECTIONAL_VECTORS = [(0,1),(1,0) ,(0,-1),(-1,0),
                       (1,1),(1,-1),(-1,1),(-1,-1)]
DIAGONAL_VECTORS = [[(1,1),(-1,-1)],[(1,-1),(-1,1)]]
DATA_FILE = "day4in.txt"
CRUX_LETTER = 'A'
AUX_LETTER_1 = 'M'
AUX_LETTER_2 = 'S'

TEST_INPUT = ["MMMSXXMASM",
              "MSAMXMSMSA",
              "AMXSXMAAMM",
              "MSAMASMSMX",
              "XMASAMXAMM",
              "XXAMMXXAMA",
              "SMSMSASXSS",
              "SAXAMASAAA",
              "MAMMMXMMMM",
              "MXMXAXMASX"]

def main():
    word = "XMAS"
    lines = open_data_file_as_lines(DATA_FILE)
    # lines = TEST_INPUT
    print(search_board_for_word(word, lines))
    print(search_board_for_x_mas(lines))

def search_for_word(word, board, coords):
    (xcoord, ycoord) = coords
    if board[xcoord][ycoord] != word[0]:
        return 0
    sum = 0
    for vector in DIRECTIONAL_VECTORS:
        if search_for_word_directionally(word, board, coords, vector):
            sum += 1
    return sum

def search_for_word_directionally(word, board, coords, vector):
    max_x = len(board)-1
    max_y = len(board[0])-1
    (vecx, vecy) = vector
    for idx, letter in enumerate(word):
        new_coords = get_new_coords(coords, vector, idx)
        if not are_coords_inbounds(new_coords, (max_x, max_y)):
            return False
        if board[new_coords[0]][new_coords[1]] != word[idx]:
            return False
    return True          

# Making a less general way to search for MAS in an X, since it's a lot more narrow
# and I want to search on the As since there is exactly one A per X-MAS
def search_board_for_x_mas(board):
    sum = 0
    for x in range(len(board)):
        # Making the assumption the board is square to save time
        for y in range(len(board[0])):
            if is_x_mas(board, (x,y)):
                sum += 1
    return sum

def is_x_mas(board, coords):
    (x,y) = coords
    if board[x][y] != CRUX_LETTER:
        return False
    max_x = len(board)-1
    max_y = len(board[0])-1
    for vector_pair in DIAGONAL_VECTORS:
        remaining_aux_1 = 1
        remaining_aux_2 = 1
        for vector in vector_pair:
            (new_x, new_y) = get_new_coords(coords, vector, 1)
            if not are_coords_inbounds((new_x, new_y), (max_x, max_y)):
                return False
            if board[new_x][new_y] == AUX_LETTER_1 and remaining_aux_1 > 0:
                remaining_aux_1 -= 1
            elif board[new_x][new_y] == AUX_LETTER_2 and remaining_aux_2 > 0:
                remaining_aux_2 -= 1
            else:
                return False
    return True

def are_coords_inbounds(coords, maximums):
    for n in [0,1]:
        if coords[n] < 0 or coords[n] > maximums[n]:
            return False
    return True

def get_new_coords(coords, vector, scale):
    return tuple(a + (b * scale) for a,b in zip(coords, vector))

def search_board_for_word(word, board):
    sum = 0
    for x in range(len(board)):
        # Making the assumption the board is square to save time
        for y in range(len(board[0])):
            sum += search_for_word(word, board, (x,y))
    return sum

main()