from itertools import product
from guroby.helpers import *
import guroby.constants as const
import gurobipy as gp
from gurobipy import GRB

# tested with Gurobi v9.1.0 and Python 3.7.0
# based on: https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/facility_location/facility_location_gcl.ipynb

class Guroby:
    def __init__(self, num_customers, num_facilities):
        self.num_customers = num_customers
        self.num_facilities = num_facilities

        customers = populate_one(num_customers)
        facilities = populate_one(num_facilities)
        self.setup_cost = populate_two(num_facilities)

        self.cartesian_prod = list(
            product(range(num_customers), range(num_facilities)))

        # Compute shipping costs
        self.shipping_cost = {(c, f): const.COST_PER_MILE*compute_distance(
            customers[c], facilities[f]) for c, f in self.cartesian_prod}

        # hide output
        env = gp.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()

        self.m = gp.Model('facility_location', env=env)

        # set different solution methods (https://www.gurobi.com/documentation/9.5/refman/method.html)
        self.m.Params.Method = 0

    def lp_lagrangian(self, multiplier):
        f_1 = sum([(self.setup_cost[f] - sum([v for k, v in multiplier.items() if k[1] == f]))
                  for f in range(self.num_facilities)])
        f_2 = sum([(self.shipping_cost[(c, f)] + multiplier[(c, f)])
                  for c in range(self.num_customers) for f in range(self.num_facilities)])

        self.m.addVars(self.num_facilities, vtype=GRB.BINARY,
                  obj=f_1, name='Select')
        assign = self.m.addVars(self.cartesian_prod,
                           vtype=GRB.BINARY, obj=f_2, name='Assign')

        self.m.addConstrs((gp.quicksum(assign[(c, f)] for f in range(
            self.num_facilities)) == 1 for c in range(self.num_customers)), name='Demand')

        # m.write('f.lp')
        self.m.optimize()

        return self.m.PoolObjVal

    def lp_relaxation(self):
        select = self.m.addVars(self.num_facilities,
                           vtype=GRB.BINARY, name='Select')
        assign = self.m.addVars(self.cartesian_prod,
                           vtype=GRB.BINARY, name='Assign')

        self.m.addConstrs((assign[(c, f)] <= select[f]
                     for c, f in self.cartesian_prod), name='Setup2ship')
        self.m.addConstrs((gp.quicksum(assign[(c, f)] for f in range(
            self.num_facilities)) == 1 for c in range(self.num_customers)), name='Demand')

        f = select.prod(self.setup_cost)+assign.prod(self.shipping_cost)
        self.m.setObjective(f, GRB.MINIMIZE)

        # (https://www.gurobi.com/documentation/9.5/refman/py_model_relax.html)
        self.m.relax()

        #m.write('f.lp')
        self.m.optimize()

        return self.m.PoolObjVal