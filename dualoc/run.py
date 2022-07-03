import guroby.guroby as guro
from algorithm.dualoc import *
from performance.helpers import *
import os, sys


def dualoc(c, f):
    print("\nDualoc solution: ")
    d = Dualoc(c, f)
    v = d.calculate_z()
    w = d.calculate_w(v)
    return d.calculate_z_s(w, v)


def simplex(c, f):
    print("\nSimplex solution: ")
    g = guro.Guroby(c, f)
    return g.simplex(1)


def relaxation(c, f):
    print("\nLinear Relaxation solution: ")
    g = guro.Guroby(c, f)
    return g.lp_relaxation()


def lagrangian(c, f):
    print("\nLagrangian Relaxation solution: ")
    d = create_multiplier(f, c)
    g = guro.Guroby(c, f)

    # calculate feasible solution
    B = g.simplex(0)
    return g.lp_lagrangian(d, 10, None, B, [])


def get_input(c, f):

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

        print(command[op](c, f))


def run():
    if len(sys.argv) < 3:
        print(
            "Usage: python3 run.py [Number of Customer] [Number of Facility]")
        return

    c = int(sys.argv[1])
    f = int(sys.argv[2])

    os.system("clear")
    print("*********************************************")
    print("*****       Dualoc Implementation       *****")
    print("*********************************************")
    print("(Info: https://github.com/matt-merman/dualoc)")

    get_input(c, f)


if __name__ == '__main__':
    run()
