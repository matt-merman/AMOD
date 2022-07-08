from guroby.guroby import *
from algorithm.dualoc import *
from performance.helpers import *
import os, sys, pyfiglet
from guroby.helpers import *
from generate.generator import * 

def dualoc(c, f, setup_cost, _, shipping_cost):
    print("\nDualoc solution: ")
    d = Dualoc(c, f, shipping_cost)
    v = d.get_z_min()
    w = d.get_w(v)
    return d.get_z_max(w, v, setup_cost)


def simplex(customer, facility, setup_cost, cartesian_prod, shipping_cost):
    print("\nSimplex solution: ")
    g = Guroby(customer, facility, setup_cost, cartesian_prod, shipping_cost)
    return g.simplex("High", "False")


def relaxation(customer, facility, setup_cost, cartesian_prod, shipping_cost):
    print("\nLinear Relaxation solution: ")
    g = Guroby(customer, facility, setup_cost, cartesian_prod, shipping_cost)
    return g.simplex("High", "True")


def lagrangian(customer, facility, setup_cost, cartesian_prod, shipping_cost):
    print("\nLagrangian Relaxation solution: ")
    d = create_multiplier(customer, facility)
    g = Guroby(customer, facility, setup_cost, cartesian_prod, shipping_cost)

    # calculate feasible solution
    B = g.simplex("Low", "False")
    return g.lp_lagrangian(d, 10, None, B, [])


def get_input(customer, facility):

    setup_interval = (1, 1000)
    customers_interval = (1, 100)

    # create random data
    generator = Generator()
    setup_cost, cartesian_prod, shipping_cost = generator.generate_instance(customer, facility, setup_interval, customers_interval)

    while True:
        try:
            op = int(input(
                "\nChoose Algorithm:\n\n1. DUALOC\n2. LP RELAXATION\n3. LP LAGRANGIAN\n4. SIMPLEX\n5. EXIT\n"))
        except ValueError:
            print("Wrong Input!")
            continue
        except KeyboardInterrupt:
            print()
            return

        if op not in [1, 2, 3, 4, 5]:
            print("Wrong Input!")
            continue

        if op == 5:
            return

        command = {1: dualoc,
                   2: relaxation,
                   3: lagrangian,
                   4: simplex,
                   }

        print(command[op](customer, facility, setup_cost, cartesian_prod, shipping_cost))


def run():
    if len(sys.argv) < 3:
        print(
            "Usage: python3 run.py [Number of Customer] [Number of Facility]")
        return

    customer = int(sys.argv[1])
    facility = int(sys.argv[2])

    os.system("clear")
    intro = pyfiglet.figlet_format("Dualoc", font="slant")
    print(intro)
    print("(Info: https://github.com/matt-merman/dualoc)")

    get_input(customer, facility)


if __name__ == '__main__':
    run()
