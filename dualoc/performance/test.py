from algorithm.dualoc import *
from guroby.guroby import *
import timeit
from performance.helpers import *
from performance.csv import *

class Test:
    def __init__(self, file, facility, customer, algorithm):
        self.facility = facility
        self.customer = customer
        self.algorithm = algorithm
        
        self.csv = CSV(file)
        self.function = {"Dualoc": self.dualoc_test, 
                         "LP_relaxation": self.relaxation_test,
                         "LP_lagrangian": self.lagrangian_test
        }

    def dualoc_test(self):
        d = Dualoc(self.facility, self.customer)
        v = d.calculate_z()
        w = d.calculate_w(v)
        return d.calculate_z_s(w, v)
    
    def relaxation_test(self):
        g = Guroby(self.facility, self.customer)
        return g.lp_relaxation() 
    
    def lagrangian_test(self):
        g = Guroby(self.facility, self.customer)
        d = create_multiplier(self.facility, self.customer)
        return g.lp_lagrangian(d)
        
    def calculate_metric(self, trial):
        mean_value = 0
        mean_time = 0
        
        for _ in range(0, trial):
            start = timeit.default_timer()
            z = self.function[self.algorithm]()
            stop = timeit.default_timer()
            
            mean_value += z
            mean_time += (stop-start)

        mean_value = mean_value/trial
        mean_time = mean_time/trial

        self.csv.add_row(trial, self.facility, self.customer, self.algorithm, mean_value, mean_time)