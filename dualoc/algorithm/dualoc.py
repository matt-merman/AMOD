from guroby.helpers import *
import guroby.constants as const
from itertools import product

class Dualoc:
    def __init__(self, num_customers, num_facilities):
        self.num_customers = num_customers
        self.num_facilities = num_facilities
        
        self.w = {}

        self.customers = populate_one(self.num_customers)
        self.facilities = populate_one(self.num_facilities)
        self.setup_cost = populate_two(self.num_facilities)
        
        self.cartesian_prod = list(product(range(self.num_customers), range(self.num_facilities)))

        # Compute shipping costs
        self.shipping_cost = {(c,f): const.COST_PER_MILE*compute_distance(self.customers[c], self.facilities[f]) for c, f in self.cartesian_prod}

    def calculate_z(self):
        values = []
        for _ in range(0, self.num_customers) : values.append(0)

        current_value = 1000
        current_customer = 0

        for key in self.shipping_cost:

            if key[0] != current_customer: 
                
                current_value = 100
                current_customer = key[0]

            new_value = self.shipping_cost[key]

            if current_value > new_value: current_value = new_value
            
            values[current_customer] = current_value

        return values

    def calculate_w(self, values):
        for v in range(0, self.num_customers):
            
            z = values[v]

            for u in range(0, self.num_facilities):

                c = self.shipping_cost.get((v, u))
                elem = max(0, z-c)
                key = (v, u)
                self.w[key] = elem
        return self.w

    def calculate_sum(self, s, u, w):
        su = 0

        for key in w:

            if key[0] == s:
                continue
            elif key[1] == u:
                su += w[key]

        return su
    
    def calculate_z_s(self, w, v):   
        z_max = []
        for _ in range(0, self.num_facilities) : z_max.append(0)

        for s in range(0, self.num_customers):

            for u in range(0, self.num_facilities):

                c = self.shipping_cost.get((s, u))
                f = self.setup_cost[u]
                summ = self.calculate_sum(s,u,w)
                z = c + f - summ
                z_max[u] = z
                #print(f"{c} + {f} - {summ} = {z}")
            
            v[s] = min(z_max)
            w = self.calculate_w(v)

        #h = len(v)
        #for i in range(h):
         #   continue
            #print(f"| {v[i]} |")
        #print(f"z = {sum(v)}")
        return sum(v)