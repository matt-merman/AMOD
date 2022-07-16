import random
from itertools import product

__all__ = ['Generator']

class Generator:
    def __init__(self):
        pass

    def get_coordinates(self, elements, lower_bound, upper_bound):
        elements_list = []
        for e in range(elements):
            x = random.uniform(lower_bound, upper_bound)
            y = random.uniform(lower_bound, upper_bound)
            element = (x, y)

            if element in elements_list:
                e-=1
                continue

            elements_list.append(element)
        return elements_list

    def generate_instance(self, customers, facilities, setup_interval, customers_interval):

        setup_cost_list = []
        for _ in range(facilities):
            setup_cost_list.append(random.uniform(
                setup_interval[0], setup_interval[1]))

        cartesian_prod_list = list(
            product(range(customers), range(facilities)))

        shipping_cost_dic = {(c, f): random.uniform(
            customers_interval[0], customers_interval[1]) for c, f in cartesian_prod_list}

        return setup_cost_list, cartesian_prod_list, shipping_cost_dic
