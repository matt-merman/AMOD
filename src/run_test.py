from performance.test import * 
from performance.chart import * 
import os, pyfiglet
from rich.console import Console
from guroby.helpers import *
from performance.helpers import *
from generate.generator import *
from performance.csv import *  

TRIAL = 10
# Do not change
FACILITIES = 2
CUSTOMERS = 15
ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = './performance/result/result.csv'


def run():

    os.system("clear")
    intro = pyfiglet.figlet_format("TEST", font="slant")
    print(intro)
    print("(Info: https://github.com/matt-merman/dualoc)")

    console = Console()
    tasks = [f"test {n}" for n in range(1, len(ALGORITHM) * TRIAL * FACILITIES * CUSTOMERS)]

    csv = CSV(PATH)
    csv.create_csv()

    generator = Generator()

    with console.status("[bold green]Working on test..."):

        for trial_interval in range(1, TRIAL * 3, TRIAL):
            
            value = time = [0] * len(ALGORITHM)

            for _ in range(trial_interval):
                setup_cost, cartesian_prod, shipping_cost = generator.generate_instance(
                    CUSTOMERS, FACILITIES)

                index = new_value = new_time = 0

                for algo in ALGORITHM:

                    task = tasks.pop(0)
                    console.log(f"[STARTING]    {task} on {algo}")

                    test = Test(CUSTOMERS, FACILITIES, algo,
                                setup_cost, cartesian_prod, shipping_cost)
                    z = test.simplex_test()

                    new_value, new_time = test.calculate_metric()
                    time.insert(index, time[index]+new_time)
                    value.insert(index, value[index]+new_value)

                    index += 1

                    console.log(f"[COMPLETED]   {task} on {algo}")

            index = 0
            for algo in ALGORITHM:

                mean_value = value[index]/trial_interval
                error = percent_error(mean_value, z)
                #print(f"{mean_value} {optimal_sol} {error}")
                mean_time = (time[index]/trial_interval)

                csv.add_row(trial_interval, CUSTOMERS, FACILITIES, algo, error, mean_time)
                index += 1
            
    chart = Chart()
    chart.error_chart(PATH)
    chart.time_chart(PATH)


if __name__ == '__main__':
    run()
