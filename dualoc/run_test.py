import performance.test as t
import performance.chart as c
import os

TRIAL = 10
NODE = 7

ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = './performance/result/result.csv'


def run():

    os.system("clear")
    print("*********************************************")
    print("*****       Dualoc Implementation       *****")
    print("*****          [Start of Test]          *****")
    print("*********************************************")

    """
    csv = t.CSV(PATH)
    csv.create_csv()

    for node in range(1, NODE):

        for algo in ALGORITHM:

            test = t.Test(PATH, node, node, algo)
            z = test.simplex_test()
            test.calculate_metric(TRIAL, z)

    """
    chart = c.Chart()
    chart.error_chart(PATH)
    chart.time_chart(PATH)


if __name__ == '__main__':
    run()
