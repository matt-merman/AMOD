# Subgradient algorithm provides a better multiplier to Lagrangian Relaxation problem
# based on note: https://www3.diism.unisi.it/~agnetis/rillag.pdf

from gurobi.helpers import *
import numpy as np
from math import sqrt


class Subgradient:
    def __init__(self, cartesian_prod, facilities, customers):
        self.cartesian_prod = cartesian_prod
        self.facilities = facilities
        self.customers = customers

    # create a matrix from the constraints
    def get_matrix(self, prod):
        A = []
        row = [0] * prod
        for facility in range(self.facilities):
            for constrain in range(self.facilities, self.cartesian_prod+self.facilities-1, self.facilities):
                row[facility] = 1
                row[constrain+facility] = -1
                A.append(row)
                row = [0] * prod

        return np.array(A)

    def get_multiplier(self, lower_bound, multiplier_dict, feasible_sol, model):

        # STEP 1: find solution (x) from that provided by lagrangian problem
        prod = self.facilities + self.cartesian_prod
        solution_array = np.array(filterDigit(prod, model))

        # STEP 2: s(h) := b−Ax(h). if s(h) == 0, STOP
        A = self.get_matrix(prod)
        # b = 0
        s = A.dot(-solution_array)
        if np.all(s == 0):
            return 0

        # STEP 3: θ(h) := B−L(λ(h−1)) / ||s(h)||^2
        s_2 = np.power(s, 2)
        s_2 = np.sum(s_2)
        # B−L(λ^(h−1))
        O = (feasible_sol - lower_bound)/s_2

        # STEP 4: λ(h+1) := λ(h) + θ(h) s(h) / ||s(h)||
        norm = sqrt(s_2)
        s_dictionary = conv2dict(self.facilities, self.customers, s)
        d = O/norm
        for key, value in s_dictionary.items():
            s_dictionary[key] = value * d
        
        new_multiplier = {key: multiplier_dict[key] + s_dictionary.get(key, 0)
                          for key in multiplier_dict.keys()}

        return new_multiplier
