import guroby.guroby as guro
from algorithm.dualoc import *
import os, sys

def run():
    if len(sys.argv) < 3:
        print("Usage: python3 run.py [Number of Customer] [Number of Facility]")
        return

    c = int(sys.argv[1])
    f = int(sys.argv[2])
    
    os.system("clear")
    print("**************************************");
    print("**       Dualoc Implementation      **");
    print("**************************************");
    try:
        op = int(input("\nChoose Algorithm:\n1. DUALOC\n2. LP RELAXATION\n3. LP LAGRANGIAN\n4. EXIT\n")) 
    except ValueError:
        print("Wrong Input!")
        return
    except KeyboardInterrupt:
        print("\n")
        return
        
    if op == 1:
        d = Dualoc(c, f)
        v = d.calculate_z()
        w = d.calculate_w(v)
        z = d.calculate_z_s(w, v)
        #d.show()
    elif op == 2:
        g = guro.Guroby(c, f)
        z = g.calculate_mip(False)
    elif op == 3:
        g = guro.Guroby(c, f)
        z = g.calculate_mip(False)
    elif op == 4:
        return 
    else:
        print("Wrong Input!")
        return
    
    print(f"z = {z}")

if __name__ == '__main__':
    run()