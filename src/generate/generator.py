import random
from itertools import product
from math import sqrt


class Generator:
    def __init__(self):
        pass

    # to determine the Euclidean distance between a facility and customer sites.
    def get_distance(self, loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return sqrt(dx*dx + dy*dy)

    def get_coordinates(self, elements, lower_bound, upper_bound):
        elements_list = []
        for _ in range(elements):
            x = random.randint(lower_bound, upper_bound)
            y = random.randint(lower_bound, upper_bound)
            element = (x, y)
            elements_list.append(element)
        return elements_list

    def generate_instance(self, customers, facilities, setup_interval, customers_interval, facilities_interval):

        setup_cost_list = []
        for _ in range(facilities):
            setup_cost_list.append(random.randint(
                setup_interval[0], setup_interval[1]))

        customers_list = self.get_coordinates(
            customers, customers_interval[0], customers_interval[1])
        facilities_list = self.get_coordinates(
            facilities, facilities_interval[0], facilities_interval[1])

        cartesian_prod_list = list(
            product(range(customers), range(facilities)))

        # Compute shipping costs
        shipping_cost_dic = {(c, f): self.get_distance(
            customers_list[c], facilities_list[f]) for c, f in cartesian_prod_list}

        return setup_cost_list, cartesian_prod_list, shipping_cost_dic
