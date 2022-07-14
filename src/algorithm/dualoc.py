# Dualoc algorithm provides an high quality Lower Bound for a UFL problem efficiently
# considering the linear relaxation and the problem's dual
# based on note: http://www3.diism.unisi.it/~agnetis/dualoc.pdf

class Dualoc:
    def __init__(self, customers, facilities, costs):
        # w = {(c,f) : max(0, z-c)}
        # see get_sum() method
        self.w = {}

        # costs = {(c,f) : cost}
        self.costs = costs
        self.customers = customers
        self.facilities = facilities

    # calculate: z_v = min{c_vu}
    def get_z_min(self):
        z_min_list = [0] * self.customers
        current_cost = float("inf")
        current_customer = 0

        # costs = {(c,f) : cost}
        for key, _ in self.costs.items():
            if key[0] != current_customer:
                current_customer = key[0]

            new_cost = self.costs[key]

            if current_cost > new_cost:
                current_cost = new_cost

            z_min_list[current_customer] = current_cost

        return z_min_list

    # calculate: w_vu = max{0,z_v − c_vu}
    def get_w(self, z_v):
        for customer in range(self.customers):

            z = z_v[customer]

            for facility in range(self.facilities):

                cost = self.costs.get((customer, facility))
                key = (customer, facility)
                self.w[key] = max(0, z-cost)

        return self.w

    # calculate: sum(w)
    def get_sum(self, customer_s, facility, w):
        summ = 0

        # w = {(c,f) : max(0, z-c)}
        for key, value in w.items():
            if key[0] == customer_s:
                continue
            elif key[1] == facility:
                summ += value

        return summ

    # calculate: z_max = min{c_su + f_u − sum(w_vu)}
    def get_z_max(self, w, v, setup_cost_list):
        z_max_list = [0] * self.facilities

        for customer in range(self.customers):
            for facility in range(self.facilities):

                cost = self.costs.get((customer, facility))
                setup_cost = setup_cost_list[facility]
                summ = self.get_sum(customer, facility, w)
                z = cost + setup_cost - summ

                z_max_list[facility] = z

            v[customer] = min(z_max_list)
            w = self.get_w(v)

        return sum(v)
