from itertools import product
from guroby.helpers import *
from guroby.subgradient import *
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

        self.select = self.m.addVars(num_facilities,
                                     vtype=GRB.BINARY, name='Select')
        self.assign = self.m.addVars(self.cartesian_prod,
                                     vtype=GRB.BINARY, name='Assign')

        self.m.addConstrs((gp.quicksum(self.assign[(c, f)] for f in range(
            num_facilities)) == 1 for c in range(num_customers)), name='Demand')

    def solve(self, obj_func):
        self.m.setObjective(obj_func, GRB.MINIMIZE)
        # self.m.write('f.lp')
        self.m.optimize()

        nSolutions = self.m.SolCount
        #print(nSolutions)
        #for e in range(nSolutions):
        self.m.setParam(GRB.Param.SolutionNumber, nSolutions - 1)
        print("############")
        print(self.m.PoolObjVal)
        print(self.m.objVal)
        print("############")

        return self.m.objVal

    def simplex(self):
        self.m.addConstrs((self.assign[(c, f)] <= self.select[f]
                           for c, f in self.cartesian_prod), name='Setup2ship')

        f = self.select.prod(self.setup_cost) + \
            self.assign.prod(self.shipping_cost)

        return self.solve(f)

    def lp_lagrangian(self, multiplier, k, lb, B):

        if (k == 0):
            return lb

        #print(lb)

        coef_1 = []
        coef_2 = {}
        lambda_sum = 0
        for f in range(self.num_facilities):
            for key, v in multiplier.items():
                if key[1] == f:
                    lambda_sum += v

            coef_1.append(self.setup_cost[f] - lambda_sum)
            lambda_sum = 0

            for c in range(self.num_customers):
                c_uv = self.shipping_cost[(c, f)]
                lambda_uv = multiplier.get(c, f)
                coef_2[(f, c)] = c_uv + lambda_uv

        f = self.select.prod(coef_1)+self.assign.prod(coef_2)
        lb = self.solve(f)

        new_multiplier = subgradient(lb, multiplier, len(
            self.cartesian_prod), self.num_facilities, self.num_customers, B, self.m)
        if new_multiplier == 0:
            return lb

        k -= 1

        return self.lp_lagrangian(new_multiplier, k, lb, B)

    def lp_relaxation(self):
        self.m.addConstrs((self.assign[(c, f)] <= self.select[f]
                           for c, f in self.cartesian_prod), name='Setup2ship')

        # see: https://www.gurobi.com/documentation/9.5/refman/py_model_relax.html
        self.m.relax()

        f = self.select.prod(self.setup_cost) + \
            self.assign.prod(self.shipping_cost)

        return self.solve(f)
