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

def is_free_block(block):
    return get_block_value(block) == 0

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
    return checksum

def process_file_part_2(line):
    blocks = []
    for i,size in enumerate(line):
        if i % 2: # if it's odd, it's free space
            blocks.append((0, int(size)))
        else:
            blocks.append((int(i/2),int(size)))
    # Using 0 to identify open blocks simplifies a lot of things
    # However, the first element is also 0.  Popping it from the list
    # and storing it to psuh back on will save lots of time
    first_block_element = blocks[0]
    blocks = blocks[1:]
    back_pointer = len(blocks) - 1
    while back_pointer > 0:
        current_block = blocks[back_pointer]
        if is_free_block(current_block):
            back_pointer -= 1
            continue
        first_open_block_pointer = get_first_open_block(blocks[:back_pointer], get_block_size(current_block))
        if first_open_block_pointer < 0:
            back_pointer -= 1
            continue
        # Replace old block
        blocks[back_pointer] = (0, get_block_size(current_block))
        free_block_size = get_block_size(blocks[first_open_block_pointer])
        blocks[first_open_block_pointer] = current_block
        back_pointer -= 1
        if get_block_size(current_block) < free_block_size:
            blocks.insert(first_open_block_pointer + 1, (0,free_block_size - get_block_size(current_block)))
            back_pointer += 1
    blocks.insert(0,first_block_element)
    return blocks



def get_first_open_block(blocks, size):
    for i, block in enumerate(blocks):
        if (is_free_block(block)) and (get_block_size(block) >= size):
            return i
    return -1

def main():
    line = open_data_file_as_lines(DATA_FILE)[0].strip()
    # line = "2333133121414131402"
    defragmented_blocks = process_file(line)
    better_fragmented_blocks = process_file_part_2(line)
    print(get_checksum(defragmented_blocks))
    print(get_checksum(better_fragmented_blocks))


main()