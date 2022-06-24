import random
from math import sqrt

def generate(max=1000):
    x = random.randint(0, max)
    return x

def populate_one(max):
    list = []
    for i in range(max):
        x = generate()
        y = generate()
        list.append((x,y))
    return list

def populate_two(max):
    list = []
    for i in range(max):
        x = generate()
        list.append(x)
    return list

# This function determines the Euclidean distance between a facility and customer sites.
def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)