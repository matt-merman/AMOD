from performance.test import *
from performance.chart import *
import os
import pyfiglet


def run():

    os.system("clear")
    intro = pyfiglet.figlet_format("TEST", font="slant")
    print(intro)
    print("(Info: https://github.com/matt-merman/dualoc)")

    Test()

    #chart = Chart()
    #chart.error_chart('./performance/result/result.csv')
    #chart.time_chart('./performance/result/result.csv')


if __name__ == '__main__':
    run()
