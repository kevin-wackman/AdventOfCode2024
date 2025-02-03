from enum import Enum
from operator import add

class Vector(Enum):
    UP = (-1,0)
    RIGHT = (0,1)
    DOWN = (1,0)
    LEFT = (0,-1)

def apply_to_tuples(fn, t1, t2):
    return (fn(t1[0], t2[0]), fn(t1[1], t2[1]))

def add_tuples(t1, t2):
    return apply_to_tuples(add, t1, t2)

def string_to_digits(str):
    return [int(char) for char in str.strip()]

def get_neighbors(coords):
    neighbors = []
    for vector in Vector:
        neighbors.append(add_tuples(coords, vector.value))
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