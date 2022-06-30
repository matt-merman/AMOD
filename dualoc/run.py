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


def relaxation(c, f):
    print("\nLinear Relaxation solution: ")
    g = guro.Guroby(c, f)
    return g.lp_relaxation()


def lagrangian(c, f):
    print("\nLagrangian Relaxation solution: ")
    d = create_multiplier(f, c)
    g = guro.Guroby(c, f)
    return g.lp_lagrangian(d)


def get_input(c, f):

    while True:
        try:
            op = int(input(
                "\nChoose Algorithm:\n\n1. DUALOC\n2. LP RELAXATION\n3. LP LAGRANGIAN\n4. EXIT\n"))
        except ValueError:
            print("Wrong Input!")
            continue
        except KeyboardInterrupt:
            print()
            return

        if op not in [1, 2, 3, 4]:
            print("Wrong Input!")
            continue

        if op == 4:
            return

        command = {1: dualoc,
                   2: relaxation,
                   3: lagrangian,
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
