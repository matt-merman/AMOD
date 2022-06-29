import random
from math import sqrt
import guroby.constants as const


def populate_one(element):
    l = []
    for _ in range(element):
        x = random.randint(1, const.MAX)
        y = random.randint(1, const.MAX)
        l.append((x, y))
    return l


def populate_two(element):
    l = []
    for _ in range(element):
        x = random.randint(1, const.MAX)
        l.append(x)
    return l

# This function determines the Euclidean distance between a facility and customer sites.


def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)
