from filehandling import open_data_file_as_lines
from collections import deque
from functools import reduce

DATA_FILE = "day9in.txt"

# A block is a tuple
# (val, size)
def get_block_value(block):
    return block[0]

def get_block_size(block):
    return block[1]

def process_file(line):
    file_blocks = deque()
    free_blocks = deque()
    for i,size in enumerate(line):
        if i % 2: # if it's odd, it's free space
            free_blocks.append(int(size))
        else:
            file_blocks.append((int(i/2),int(size)))
    defragmented_blocks = []
    while len(file_blocks):
        # In the loop, process one file block and one free block
        defragmented_blocks.append(file_blocks.popleft())
        # Process the free block
        free_block_size = free_blocks.popleft()
        while free_block_size > 0:
            if not len(file_blocks):
                return defragmented_blocks
            # Handling an edge case - not 100% necessary for step 1, but leads to a more accurate 
            # representation of the blocks
            if len(file_blocks) == 1:
                defragmented_blocks.append(file_blocks.pop())
                return defragmented_blocks
            right_block = file_blocks.pop()
            if get_block_size(right_block) <= free_block_size:
                defragmented_blocks.append(right_block)
                free_block_size -= get_block_size(right_block)
            else:
                defragmented_blocks.append((get_block_value(right_block), free_block_size))
                leftover_block_size = get_block_size(right_block) - free_block_size
                file_blocks.append((get_block_value(right_block), leftover_block_size))
                free_block_size = 0
    return defragmented_blocks

def get_checksum(blocks):
    checksum_list = [get_block_value(block) for block in blocks for _ in range(get_block_size(block))]
    checksum = reduce(lambda total, n: total + n[0] * n[1], enumerate(checksum_list), 0)
    print(checksum)




def main():
    line = open_data_file_as_lines(DATA_FILE)[0].strip()
    #line = "2333133121414131402"
    defragmented_blocks = process_file(line)
    get_checksum(defragmented_blocks)


main()