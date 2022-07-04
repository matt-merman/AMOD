# Tested with Gurobi v9.1.0 and Python 3.7.0
# Guroby class provides 3 solving methods:
# 1. Simplex method
# 2. Lagrangian Relaxation
# 3. Linear Relaxation

# based on demo: https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/facility_location/facility_location_gcl.ipynb

from guroby.helpers import *
from guroby.subgradient import *
import gurobipy as gp
from gurobipy import GRB


class Guroby:
    def __init__(self, customers, facilities, setup_cost, cartesian_prod, shipping_cost):
        self.customers = customers
        self.facilities = facilities
        self.setup_cost = setup_cost
        self.cartesian_prod = cartesian_prod
        self.shipping_cost = shipping_cost

        # to hide the output
        env = gp.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()

        self.model = gp.Model('facility_location', env=env)

        # to set primal simplex algorithm 
        # (https://www.gurobi.com/documentation/9.5/refman/method.html)
        self.model.Params.Method = 0

        self.select = self.model.addVars(facilities,
                                         vtype=GRB.BINARY, name='Select')
        self.assign = self.model.addVars(self.cartesian_prod,
                                         vtype=GRB.BINARY, name='Assign')

        print(self.customers)
        print(self.facilities)

        self.model.addConstrs((gp.quicksum(self.assign[(customer, facility)] for facility in range(facilities)) == 1 for customer in range(customers)), name='Demand')

        # to disactivate presolve options and others 
        # (https://support.gurobi.com/hc/en-us/community/posts/360048467412-Separating-specific-cuts)
        self.model.setParam(GRB.Param.Presolve, 0)
        self.model.setParam(GRB.Param.Cuts, 0)
        self.model.setParam(GRB.Param.Heuristics, 0)

    def solve(self, obj_func, quality):
        self.model.setObjective(obj_func, GRB.MINIMIZE)
        # self.m.write('f.lp')
        self.model.optimize()

        nSolutions = self.model.SolCount
        self.model.setParam(GRB.Param.SolutionNumber, nSolutions-1)

        if quality == "Low":
            return self.model.PoolObjVal
        else:
            return self.model.objVal

    def simplex(self, quality, relax):

        self.model.addConstrs((self.assign[(customer, facility)] <= self.select[facility]
                               for customer, facility in self.cartesian_prod), name='Setup2ship')

        # calculate the linear relaxation solution
        if relax == True:
            self.model.relax()

        obj_func = self.select.prod(self.setup_cost) + \
            self.assign.prod(self.shipping_cost)

        return self.solve(obj_func, quality)

    # calculate the lagrangian relaxation solution
    # relaxing only the x_u > y_uv constraits
    def lp_lagrangian(self, multiplier_dict, iterations, lower_bound, feasible_sol, result):

        # check if the lower bound has not improved in the last iterations
        if check_lastest_result(result, iterations):
            return lower_bound

        # firt coefficient in the obj func
        coef_1 = []
        # second coefficient in the obj func
        coef_2 = {}

        lambda_sum = 0
        for facility in range(self.facilities):
            # multiplier_dict = {(c,f) : lambda}
            for key, value in multiplier_dict.items():
                if key[1] == facility:
                    lambda_sum += value

            coef_1.append(self.setup_cost[facility] - lambda_sum)
            lambda_sum = 0
            for customer in range(self.customers):

                key = (customer, facility)
                cost = self.shipping_cost[key]
                value = multiplier_dict.get(customer, facility)
                coef_2[key] = cost + value

                #######################
                # KEEP ATTENTION before it was inverted (need to test)
                #coef_2[(facility, customer)] = cost + lambda_uv

        obj_func = self.select.prod(coef_1)+self.assign.prod(coef_2)
        lower_bound = self.solve(obj_func, 1)

        # use subgradient algorithm to find a better multiplier
        sub = Subgradient(len(self.cartesian_prod),
                          self.facilities, self.customers)
        new_multiplier_dict = sub.get_multiplier(
            lower_bound, multiplier_dict, feasible_sol, self.model)

        if new_multiplier_dict == 0:
            return lower_bound

        iterations -= 1

        result.append(lower_bound)
        return self.lp_lagrangian(new_multiplier_dict, iterations, lower_bound, feasible_sol, result)
