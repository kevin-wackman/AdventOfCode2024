from filehandling import open_data_file_as_lines

DIRECTIONAL_VECTORS = [(0,1),(1,0) ,(0,-1),(-1,0),
                       (1,1),(1,-1),(-1,1),(-1,-1)]

DATA_FILE = "day4in.txt"

def main():
    word = "XMAS"
    lines = open_data_file_as_lines(DATA_FILE)
    print(search_board_for_word(word, lines))

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