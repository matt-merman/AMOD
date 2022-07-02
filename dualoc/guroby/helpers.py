import random
import re
from math import sqrt
import guroby.constants as const


def conv2dict(fac, cust, s):

    d = {}
    for i in range(fac):
        for j in range(cust):
            key = (j, i)
            value = s[2*i+j]
            d[key] = value

    return d


def filterDigit(len, model):
    digitList = []
    pattern_one = re.compile(r' \d.\d')
    pattern_two = re.compile(r'-\d.\d')
    for i in range(len):

        s = str(model.getVars()[i])
        mo = pattern_one.search(s)
        if mo == None:
            mo = pattern_two.search(s)

        digitList.append(int(mo.group()[1]))

    return digitList


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
