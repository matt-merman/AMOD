from guroby.helpers import *
import guroby.constants as const
from algorithm.dualoc import *

def run():
    d = Dualoc(num_customers=const.CUSTOMERS, num_facilities=const.FACILITIES)
    v = d.calculate_z()
    w = d.calculate_w(v)
    d.calculate_z_s(w, v)
    d.show()

if __name__ == '__main__':
    run()