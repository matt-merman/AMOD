import performance.test as t
import performance.chart as c
import os
from rich.console import Console
from itertools import product
from guroby.helpers import *
from performance.helpers import *

TRIAL = 10
# Do not change
NODE = 15

ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = './performance/result/result.csv'


def generate_instance(num_customers, num_facilities):
    customers = populate_one(num_customers)
    facilities = populate_one(num_facilities)
    setup_cost = populate_two(num_facilities)

    cartesian_prod = list(
        product(range(num_customers), range(num_facilities)))

    # Compute shipping costs
    shipping_cost = {(c, f): const.COST_PER_MILE*compute_distance(
        customers[c], facilities[f]) for c, f in cartesian_prod}

    return setup_cost, cartesian_prod, shipping_cost


def run():

    
    os.system("clear")
    print("*********************************************")
    print("*****       Dualoc Implementation       *****")
    print("*****          [Start of Test]          *****")
    print("*********************************************")

    console = Console()
    tasks = [f"test {n}" for n in range(1, (NODE-1) * len(ALGORITHM) * TRIAL)]

    csv = t.CSV(PATH)
    csv.create_csv()

    with console.status("[bold green]Working on test...") as status:
        for node in range(9, NODE):
            
            time = []
            for _ in range(0, len(ALGORITHM)) : time.append(0)
            value = []
            for _ in range(0, len(ALGORITHM)) : value.append(0)

            for trial in range(TRIAL):
                setup_cost, cartesian_prod, shipping_cost = generate_instance(
                    node, node)

                index = 0
                new_value = 0
                new_time = 0

                for algo in ALGORITHM:

                    task = tasks.pop(0)
                    console.log(f"[STARTING]    {task} on {algo}")

                    test = t.Test(PATH, node, node, algo,
                                  setup_cost, cartesian_prod, shipping_cost)
                    z = test.simplex_test()
                    
                    new_value, new_time = test.calculate_metric(z)
                    time.insert(index, time[index]+new_time)
                    value.insert(index, value[index]+new_value)

                    index+=1

                    console.log(f"[COMPLETED]   {task} on {algo}")
            
            index = 0
            for algo in ALGORITHM:

                mean_value = value[index]/(trial+1)   
                error = percent_error(mean_value, z)
                #print(f"{mean_value} {optimal_sol} {error}")
                mean_time = (time[index]/(trial+1)) * 1000

                csv.add_row(trial+1, node, node,
                                algo, error, mean_time)
                index+=1
    
    chart = c.Chart()
    chart.error_chart(PATH)
    chart.time_chart(PATH)


if __name__ == '__main__':
    run()
