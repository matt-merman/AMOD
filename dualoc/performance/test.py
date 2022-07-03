from algorithm.dualoc import *
from guroby.guroby import *
import timeit
from performance.helpers import *
from performance.csv import *


class Test:
    def __init__(self, file, facility, customer, algorithm, setup_cost, cartesian_prod, shipping_cost):
        self.facility = facility
        self.customer = customer
        self.algorithm = algorithm

        self.setup_cost = setup_cost
        self.cartesian_prod = cartesian_prod
        self.shipping_cost = shipping_cost

        self.csv = CSV(file)
        self.function = {"Dualoc": self.dualoc_test,
                         "LP_relaxation": self.relaxation_test,
                         "LP_lagrangian": self.lagrangian_test,
                         "Simplex": self.simplex_test
                         }

    def dualoc_test(self):
        d = Dualoc(self.facility, self.customer, self.setup_cost, self.cartesian_prod, self.shipping_cost)
        v = d.calculate_z()
        w = d.calculate_w(v)
        return d.calculate_z_s(w, v)

    def simplex_test(self):
        g = Guroby(self.facility, self.customer, self.setup_cost, self.cartesian_prod, self.shipping_cost)
        return g.simplex(1)

    def relaxation_test(self):
        g = Guroby(self.facility, self.customer, self.setup_cost, self.cartesian_prod, self.shipping_cost)
        return g.lp_relaxation()

    def lagrangian_test(self):
        g = Guroby(self.facility, self.customer, self.setup_cost, self.cartesian_prod, self.shipping_cost)
        d = create_multiplier(self.facility, self.customer)
        
        B = g.simplex(0)
        
        return g.lp_lagrangian(d, 10, None, B, [])

    def calculate_metric(self, optimal_sol):
        mean_value = 0
        mean_time = 0

        #for _ in range(0, trial):
        start = timeit.default_timer()
        z = self.function[self.algorithm]()
        stop = timeit.default_timer()

        return z, (stop-start)
        """
        mean_value += z
        mean_time += (stop-start)

        mean_value = mean_value/trial
        error = percent_error(mean_value, optimal_sol)
        #print(f"{mean_value} {optimal_sol} {error}")
        mean_time = (mean_time/trial) * 1000

        self.csv.add_row(trial, self.facility, self.customer,
                         self.algorithm, error, mean_time)
        """