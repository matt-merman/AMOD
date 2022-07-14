from performance.test import *
from performance.chart import *
import os
import pyfiglet


def run():

    os.system("clear")
    intro = pyfiglet.figlet_format("TEST", font="slant")
    print(intro)
    print("(Info: https://github.com/matt-merman/amod)")

    Test()

if __name__ == '__main__':
    run()
