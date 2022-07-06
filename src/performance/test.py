from performance.algorithm import *
from rich.console import Console
from performance.helpers import *
from generate.generator import *
from performance.csv import *
from statistics import variance


class Test:
    def __init__(self):
        self.tests = {0: self.test_one,
                      1: self.test_two,
                      2: self.test_three,
                      3: self.test_four,
                      4: self.test_five
                      }
        self.trial = 10
        # Do not change
        self.facilities = 2
        self.customers = 3
        self.algorithm = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
        self.path = './performance/result/result.csv'

        csv = CSV(self.path)
        csv.create_csv()

        console = Console()
        tasks = [f"test {n}" for n in range(
            1, len(self.algorithm) * self.trial*6 * self.facilities * self.customers)]

        for t in range(0, 1):

            with console.status("[bold green]Working on test..."):
                for trial_interval in range(1, self.trial*6, self.trial):

                    time = [0] * len(self.algorithm)
                    value = [0] * len(self.algorithm)

                    index = 0
                    for algo in self.algorithm:

                        new_value = 0
                        new_time = 0

                        for _ in range(trial_interval):

                            setup_interval, customers_interval, facilities_interval = self.tests[t](
                            )

                            #sample1 = (1412, 900)
                            # print(variance(sample1))

                            generator = Generator()
                            setup_cost, cartesian_prod, shipping_cost = generator.generate_instance(
                                self.customers, self.facilities, setup_interval, customers_interval, facilities_interval)

                            #print(setup_cost)
                            #print(shipping_cost)

                            #return

                            task = tasks.pop(0)
                            console.log(f"[STARTING]    {task} on {algo}")

                            test = Algorithm(self.customers, self.facilities, algo,
                                             setup_cost, cartesian_prod, shipping_cost)
                            z = test.simplex_test()

                            new_value, new_time = test.calculate_metric()
                            time[index] += new_time
                            value[index] += new_value

                            console.log(f"[COMPLETED]   {task} on {algo}")

                        mean_value = (value[index]/trial_interval)
                        error = percent_error(mean_value, z)
                        mean_time = (time[index]/trial_interval)*1000

                        csv.add_row(trial_interval, self.customers,
                                    self.facilities, algo, error, mean_time)

                        index += 1

    # TEST CASE 3: setup cost ~ shipping cost
    def test_one(self):

        ub_setup_cost = 100
        lb_setup_cost = ub_setup_cost * .9

        lb_customer = lb_setup_cost
        ub_customer = ub_setup_cost

        lb_facility = 1
        ub_facility = ub_setup_cost * .1

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)
        facilities_interval = (lb_facility, ub_facility)

        return setup_interval, customers_interval, facilities_interval

    # TEST CASE 2: setup cost >> shipping cost
    # minimun value for shipping cost: 1.5% of setup cost
    # maximun value for shipping cost: 12% of setup cost
    def test_two(self):

        ub_setup_cost = 1000
        lb_setup_cost = ub_setup_cost * .9

        lb_facility = 1
        ub_facility = ub_setup_cost * .1

        lb_customer = lb_facility + 1
        ub_customer = ub_setup_cost * .1

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)
        facilities_interval = (lb_facility, ub_facility)

        return setup_interval, customers_interval, facilities_interval

    # TEST CASE 3: setup cost << shipping cost
    # minimun value for shipping cost: 1.5% of setup cost
    # maximun value for shipping cost: 12% of setup cost

    # TO-DO
    def test_three(self):

        ub_setup_cost = 1000
        lb_setup_cost = ub_setup_cost * .1

        ub_facility = 1000
        lb_facility = ub_facility * .9

        ub_customer = 1000
        lb_customer = (ub_customer * .9) + 1

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)
        facilities_interval = (lb_facility, ub_facility)

        return setup_interval, customers_interval, facilities_interval

    # TEST CASE 4: high variance in setup cost/low variance in shipping cost
    # maximun value for variance in shipping cost: 2*10^4
    # maximun value for variance in setup cost: 5 * 10^6
    def test_four(self):

        ub_setup_cost = 1000
        lb_setup_cost = 1

        lb_facility = 1
        ub_facility = 1

        lb_customer = lb_facility + 1
        ub_customer = ub_setup_cost * .2

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)
        facilities_interval = (lb_facility, ub_facility)

        return setup_interval, customers_interval, facilities_interval

    # TEST CASE 5: low variance in setup cost/high variance in shipping cost
    # maximun value for variance in shipping cost: 9 * 10^6
    # maximun value for variance in setup cost: 5 * 10^3
    def test_five(self):

        ub_setup_cost = 1000
        lb_setup_cost = ub_setup_cost * .9

        lb_facility = 1
        ub_facility = ub_setup_cost

        lb_customer = lb_facility + 1
        ub_customer = ub_setup_cost

        setup_interval = (lb_setup_cost, ub_setup_cost)
        customers_interval = (lb_customer, ub_customer)
        facilities_interval = (lb_facility, ub_facility)

        return setup_interval, customers_interval, facilities_interval
