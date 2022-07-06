from algorithm.dualoc import *
from guroby.guroby import *
import timeit
from performance.helpers import *


class Algorithm:
    def __init__(self, customers, facilities, algorithm, setup_cost, cartesian_prod, shipping_cost):
        self.facilities = facilities
        self.customers = customers
        self.algorithm = algorithm
        self.setup_cost = setup_cost
        self.cartesian_prod = cartesian_prod
        self.shipping_cost = shipping_cost

        self.function = {"Dualoc": self.dualoc_test,
                         "LP_relaxation": self.relaxation_test,
                         "LP_lagrangian": self.lagrangian_test,
                         "Simplex": self.simplex_test
                         }

    def dualoc_test(self):
        d = Dualoc(self.customers, self.facilities, self.shipping_cost)
        v = d.get_z_min()
        w = d.get_w(v)
        return d.get_z_max(w, v, self.setup_cost)

    def simplex_test(self):
        g = Guroby(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)
        return g.simplex("High", "False")

    def relaxation_test(self):
        g = Guroby(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)
        return g.simplex("High", "True")

    def lagrangian_test(self):
        d = create_multiplier(self.customers, self.facilities)
        g = Guroby(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)

        # calculate feasible solution
        B = g.simplex("Low", "False")
        return g.lp_lagrangian(d, 10, None, B, [])

    def calculate_metric(self):

        start = timeit.default_timer()
        z = self.function[self.algorithm]()
        stop = timeit.default_timer()

        return z, (stop-start)
