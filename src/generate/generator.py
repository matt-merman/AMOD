import random
from itertools import product
from math import sqrt

MAX = 5
COST_PER_MILE = 1


class Generator:
    def __init__(self):
        pass

        # to determine the Euclidean distance between a facility and customer sites.
    def compute_distance(self, loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return sqrt(dx*dx + dy*dy)

    def populate_one(self, element):
        l = []
        for _ in range(element):
            x = random.randint(1, MAX)
            y = random.randint(1, MAX)
            l.append((x, y))
        return l

    def populate_two(self, element):
        l = []
        for _ in range(element):
            x = random.randint(1, MAX)
            l.append(x)
        return l

    def generate_instance(self, customers, facilities):
        customers_list = self.populate_one(customers)
        facilities_list = self.populate_one(facilities)
        setup_cost_list = self.populate_two(facilities)

        cartesian_prod_list = list(
            product(range(customers), range(facilities)))

        # Compute shipping costs
        shipping_cost_dic = {(c, f): COST_PER_MILE*self.compute_distance(
            customers_list[c], facilities_list[f]) for c, f in cartesian_prod_list}

        return setup_cost_list, cartesian_prod_list, shipping_cost_dic
