from itertools import product
from helpers import *
import constants as const 
import gurobipy as gp
from gurobipy import GRB

# tested with Gurobi v9.1.0 and Python 3.7.0

class Guroby:
    def __init__(self, num_customers, num_facilities):
        self.num_customers = num_customers
        self.num_facilities = num_facilities

        self.customers = populate_one(self.num_customers)
        self.facilities = populate_one(self.num_facilities)
        self.setup_cost = populate_two(self.num_facilities)
        
        self.cartesian_prod = list(product(range(self.num_customers), range(self.num_facilities)))

        # Compute shipping costs
        self.shipping_cost = {(c,f): const.COST_PER_MILE*compute_distance(self.customers[c], self.facilities[f]) for c, f in self.cartesian_prod}

    # MIP  model formulation
    def calculate_mip(self):

        m = gp.Model('facility_location')

        select = m.addVars(self.num_facilities, vtype=GRB.BINARY, name='Select')
        assign = m.addVars(self.cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

        m.addConstrs((assign[(c,f)] <= select[f] for c,f in self.cartesian_prod), name='Setup2ship')
        m.addConstrs((gp.quicksum(assign[(c,f)] for f in range(self.num_facilities)) == 1 for c in range(self.num_customers)), name='Demand')

        m.setObjective(select.prod(self.setup_cost)+assign.prod(self.shipping_cost), GRB.MINIMIZE)

        # set different solution methods (https://www.gurobi.com/documentation/9.5/refman/method.html)
        #m.Params.Method = 0

        # https://www.gurobi.com/documentation/9.5/refman/py_model_relax.html
        #m = m.relax()

        m.optimize()

        # display optimal values of decision variables

        #for facility in select.keys():
        #   if (abs(select[facility].x) > 1e-6):
                #print(f"\n Build a warehouse at location {facility + 1}.")

        # Shipments from facilities to customers.

        #for customer, facility in assign.keys():
        #   if (abs(assign[customer, facility].x) > 1e-6):
                #print(f"\n Supermarket {customer + 1} receives {round(100*assign[customer, facility].x, 2)} % of its demand  from Warehouse {facility + 1} .")

g = Guroby(num_customers=const.CUSTOMERS, num_facilities=const.FACILITIES)
g.calculate_mip()