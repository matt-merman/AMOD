from guroby.helpers import *
import numpy as np
from math import sqrt


def subgradient(lb, multiplier, num_cartesian_prod, num_facilities, num_customers, B, model):

    # STEP 2
    l = num_facilities + num_cartesian_prod
    x = filterDigit(l, model)

    # STEP 3
    A = []
    row = [0] * l

    for i in range(num_facilities):
        for j in range(num_facilities, num_cartesian_prod+num_facilities-1, num_facilities):
            row[i] = 1
            row[j+i] = -1
            A.append(row)
            row = [0] * l

    # calculate s(h)
    A = np.array(A)
    x = np.array(x)
    # s(h) := b−Ax(h)
    s = A.dot(-x)

    if np.all((s == 0)):
        return 0

    # STEP 4
    s_2 = np.power(s, 2)

    # B−L(λ^(h−1))
    O = (B - lb)/np.sum(s_2)

    # STEP 5
    c = sqrt(np.sum(s_2))

    # convert s in dictionary
    s_dictionary = conv2dict(num_facilities, num_customers, s)

    for key, _ in s_dictionary.items():
        prev = s_dictionary[key]
        s_dictionary[key] = prev * (O/c)

    new_multiplier = {key: multiplier[key] + s_dictionary.get(key, 0)
                      for key in multiplier.keys()}

    return new_multiplier
