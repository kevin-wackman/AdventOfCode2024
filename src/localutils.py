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
