from itertools import product
from math import sqrt

from helpers import *
import constants as c 

import gurobipy as gp
from gurobipy import GRB

# tested with Gurobi v9.1.0 and Python 3.7.0

customers = []
facilities = []
setup_cost = []

customers = populate_one(customers, c.INSTANCES)
facilities = populate_one(facilities, c.INSTANCES)
setup_cost = populate_two(setup_cost, c.INSTANCES)

# Parameters
for i in range(INSTANCES):
    x = generate()
    y = generate()
    customers.append((x,y))

for i in range(INSTANCES):
    x = generate()
    y = generate()
    facilities.append((x,y))

for i in range(INSTANCES):
    x = generate()
    setup_cost.append(x)

#customers = [(0,1.5), (2.5,1.2), (1,1), (1,2), (1,3.4), (2,5.6), (0,1), (0,0), (4,1), (7,1), (2,3), (3,4), (4,5), (6,7), (5,9)]
#facilities = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), ]
#setup_cost = [3,2,3,1,3,3,4,3,2]
cost_per_mile = 1

# This function determines the Euclidean distance between a facility and customer sites.

def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)

# Compute key parameters of MIP model formulation

num_facilities = len(facilities)
num_customers = len(customers)
cartesian_prod = list(product(range(num_customers), range(num_facilities)))

# Compute shipping costs

shipping_cost = {(c,f): cost_per_mile*compute_distance(customers[c], facilities[f]) for c, f in cartesian_prod}

# MIP  model formulation

m = gp.Model('facility_location')

select = m.addVars(num_facilities, vtype=GRB.BINARY, name='Select')
assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
m.addConstrs((gp.quicksum(assign[(c,f)] for f in range(num_facilities)) == 1 for c in range(num_customers)), name='Demand')

m.setObjective(select.prod(setup_cost)+assign.prod(shipping_cost), GRB.MINIMIZE)

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
