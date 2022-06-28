import performance.test as t
import performance.chart as c

TRIAL = 700
NODE = 20
ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = ['./performance/result.csv', './performance/mean_result.csv']

def run():  

    """
    for path in PATH:
            
        csv = t.CSV(path)
        csv.create_csv()
        
    for algo in ALGORITHM:

        for node in range(2, NODE):
            
            test = t.Test(PATH[0], node, node, algo)
            test.general()
        
        for trial in range(100, TRIAL, 100):
        
            test = t.Test(PATH[1], NODE, NODE, algo)
            test.average(trial)
    """
    chart = c.Chart()
    chart.create('./performance/mean_result.csv', 'value')
    #chart.create('./performance/mean_result.csv', 'time')

if __name__ == '__main__':
    run()
