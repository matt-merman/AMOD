from algorithm.dualoc import *
from gurobi.gurobi import *
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
        
        #params for lagrangian relaxation
        self.k = 100
    
    def dualoc_test(self):
        d = Dualoc(self.customers, self.facilities, self.shipping_cost)
        v = d.get_z_min()
        w = d.get_w(v)
        return d.get_z_max(w, v, self.setup_cost)

    def simplex_test(self):
        g = Gurobi(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)
        return g.simplex(False)

    def relaxation_test(self):
        g = Gurobi(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)
        return g.simplex(True)

    def lagrangian_test(self):
        d = create_multiplier(self.customers, self.facilities)
        g = Gurobi(self.customers, self.facilities, self.setup_cost,
                   self.cartesian_prod, self.shipping_cost)

        # calculate feasible solution
        b = g.simplex(False)
        return g.lp_lagrangian(d, self.k, None, b, [])

    def calculate_metric(self):

        start = timeit.default_timer()
        z = self.function[self.algorithm]()
        stop = timeit.default_timer()

        return z, (stop-start)
