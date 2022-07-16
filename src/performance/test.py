from performance.algorithm import *
from rich.console import Console
from performance.helpers import *
from generate.generator import *
from performance.csv import *
from performance.chart import *

__all__ = ['Test']


class Test:
    def __init__(self):
        self.tests = {0: self.test_one,
                      1: self.test_two,
                      2: self.test_three,
                      3: self.test_four,
                      4: self.test_five
                      }
        self.trial = 100
        self.algorithm = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
        self.path = './performance/result/'
        self.max = 1000

        #(facilities, customers)
        self.nodes = [(30, 30), (29, 5), (5, 29)]

        console = Console()
        tasks = [f"test {n}" for n in range(
            1, len(self.tests) * len(self.algorithm) * self.trial * len(self.nodes) + 1)]

        for t in range(0, len(self.tests)):

            local_path = self.path + 'result_test_' + str(t) + '.csv'
            csv = CSV(local_path)
            csv.create_csv()

            for n in range(0, len(self.nodes)):

                with console.status("[bold green]Working on test..."):

                    time = [0] * len(self.algorithm)
                    value = [0] * len(self.algorithm)

                    index = 0
                    for algo in self.algorithm:

                        new_value = 0
                        new_time = 0

                        for _ in range(self.trial):

                            setup_interval, customers_interval = self.tests[t](
                            )

                            generator = Generator()
                            setup_cost, cartesian_prod, shipping_cost = generator.generate_instance(
                                self.nodes[n][1], self.nodes[n][0], setup_interval, customers_interval)

                            task = tasks.pop(0)
                            console.log(f"[STARTING]    {task} on {algo}")

                            test = Algorithm(self.nodes[n][1], self.nodes[n][0], algo,
                                             setup_cost, cartesian_prod, shipping_cost)
                            z = test.simplex_test()

                            new_value, new_time = test.calculate_metric()
                            time[index] += new_time
                            value[index] += new_value

                            console.log(f"[COMPLETED]   {task} on {algo}")

                        mean_value = (value[index]/self.trial)
                        error = percent_error(mean_value, z)
                        mean_time = (time[index]/self.trial)*1000

                        csv.add_row(self.trial, self.nodes[n][0],
                                    self.nodes[n][1], algo, error, mean_time)

                        index += 1

            chart = Chart()

            chart.error_chart(local_path, self.path +
                              'chart_error_' + str(t) + '.png', ["Dualoc", "LP_relaxation", "LP_lagrangian"], 0.25)
            chart.time_chart(local_path,  self.path +
                             'chart_time_' + str(t) + '.png', ["Dualoc", "LP_relaxation", "LP_lagrangian"], 0.25)

            chart.error_chart(local_path, self.path +
                              'chart_error_lagrangian_' + str(t) + '.png', ["LP_lagrangian"], 0.12)
            chart.time_chart(local_path,  self.path +
                             'chart_time_lagrangian_' + str(t) + '.png', ["LP_lagrangian"], 0.12)

    # TEST CASE 1: setup cost = shipping cost
    # worth case: ratio(shipping cost/setup cost) = 950/1000 ~ 1

    def test_one(self):

        ub_setup_cost = self.max
        lb_setup_cost = ub_setup_cost * .95

        ub_customer = ub_setup_cost
        lb_customer = ub_setup_cost * .95

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        return setup_interval, customers_interval

    # TEST CASE 2: setup cost >> shipping cost
    # worth case: ratio(shipping cost/setup cost) = 100/950 ~ 1/10
    # best case: ratio(shipping cost/setup cost) = 1/1000
    def test_two(self):

        ub_setup_cost = self.max
        lb_setup_cost = ub_setup_cost * .95

        ub_customer = ub_setup_cost * .10
        lb_customer = 1

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        return setup_interval, customers_interval

    # TEST CASE 3: setup cost << shipping cost
    # worth case: ratio(shipping cost/setup cost) = 95 ~ 100
    # best case: ratio(shipping cost/setup cost) = 1000
    def test_three(self):

        ub_customer = self.max
        lb_customer = ub_customer * .95

        ub_setup_cost = ub_customer * .10
        lb_setup_cost = 1

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        return setup_interval, customers_interval

    # TEST CASE 4: high variance in setup cost/low variance in shipping cost
    # max variance in setup cost = 125'000
    # max variance in shipping cost = 5'000
    def test_four(self):

        ub_setup_cost = self.max
        lb_setup_cost = ub_setup_cost * .50

        lb_customer = ub_setup_cost * .10
        ub_customer = ub_setup_cost * .20

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        return setup_interval, customers_interval

    # TEST CASE 5: low variance in setup cost/high variance in shipping cost
    # max variance in setup cost = 5'000
    # max variance in shipping cost = 125'000
    def test_five(self):

        ub_setup_cost = self.max
        lb_setup_cost = ub_setup_cost * .90

        lb_customer = ub_setup_cost * .50
        ub_customer = ub_setup_cost

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)

        return setup_interval, customers_interval
