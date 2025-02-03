from enum import Enum
from operator import add
import re

class Vector(Enum):
    UP = (-1,0)
    RIGHT = (0,1)
    DOWN = (1,0)
    LEFT = (0,-1)

def rotate_clockwise(vec):
    match vec:
        case Vector.UP:
            return Vector.RIGHT
        case Vector.RIGHT:
            return Vector.DOWN
        case Vector.DOWN:
            return Vector.LEFT
        case Vector.LEFT:
            return Vector.UP
    raise ValueError("Invalid vector {} found".format(vec))

def apply_to_tuples(fn, t1, t2):
    return (fn(t1[0], t2[0]), fn(t1[1], t2[1]))

def add_tuples(t1, t2):
    return apply_to_tuples(add, t1, t2)

def apply_vector(coords, vec):
    return add_tuples(coords, vec.value)

def string_to_digits(str):
    return [int(char) for char in str.strip()]

def get_neighbors(coords):
    return [neighbor for (_, neighbor) in get_neighbors_with_direction(coords)]

def get_neighbors_with_direction(coords):
    neighbors = []
    for vector in Vector:
        neighbors.append((vector, add_tuples(coords, vector.value)))
    return neighbors

def is_in_bounds(map, coords):
    max_x = len(map)
    max_y = len(map[0])
    (x,y) = coords
    if (x < 0 or x >= max_x):
        return False
    return (y >= 0 and y < max_y)

def get_position(map, coords):
    return map[coords[0]][coords[1]]

def extract_ints(string):
    # Regular expression lovingly provided by chatGPT    
    return list(map(int, re.findall(r'\d+', string)))  # Extract numbers and convert to integers