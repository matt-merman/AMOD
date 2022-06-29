from algorithm.dualoc import *
from guroby.guroby import *
import csv, timeit
from performance.helpers import *

class CSV:
    def __init__(self, file):
        self.file = file

    def create_csv(self):

        header = ['#trial', '#facility', '#customer', 'algorithm', 'value', 'time']
        f = open(self.file, 'w')
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    
    def add_row(self, trial, facility, customer, algorithm, value, time):
        list_data=[trial, facility, customer, algorithm, value, time]
        
        with open(self.file, 'a', newline='') as f_object:  
            writer_object = csv.writer(f_object)
            writer_object.writerow(list_data)  
            f_object.close()
    
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
        
    def general(self):
        start = timeit.default_timer()
        z = self.function[self.algorithm]()
        stop = timeit.default_timer()
        
        self.csv.add_row('NULL', self.facility, self.customer, self.algorithm, z, stop-start)
    
    def average(self, trial):
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