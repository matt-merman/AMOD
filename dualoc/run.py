import guroby.constants as const
import guroby.guroby as guro
from algorithm.dualoc import *
import os

def run():
    os.system("clear")
    print("**************************************");
    print("**       Dualoc Implementation      **");
    print("**************************************");
    try:
        op = int(input("\nChoose operation:\n1. DUALOC\n2. LP RELAXATION\n3. LP LAGRANGIAN\n4. EXIT\n")) 
    except ValueError:
        print("Wrong Input!")
        return
        
    if op == 1:
        d = Dualoc(const.CUSTOMERS, const.FACILITIES)
        v = d.calculate_z()
        w = d.calculate_w(v)
        z = d.calculate_z_s(w, v)
        #d.show()
    elif op == 2:
        g = guro.Guroby(const.CUSTOMERS, const.FACILITIES)
        z = g.calculate_mip(False)
    elif op == 3:
        g = guro.Guroby(const.CUSTOMERS, const.FACILITIES)
        z = g.calculate_mip(False)
    elif op == 4:
        return 
    else:
        print("Wrong Input!")
        return
    
    print(f"z = {z}")

if __name__ == '__main__':
    run()