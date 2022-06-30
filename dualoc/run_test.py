import performance.test as t
import performance.chart as c

TRIAL = 1000
NODE = 8
ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = './performance/result/result.csv'

def run():  
            
    csv = t.CSV(PATH)
    csv.create_csv()
        
    for algo in ALGORITHM:

        for node in range(2, NODE):
        
            test = t.Test(PATH, node, node, algo)
            test.calculate_metric(TRIAL)
    
    chart = c.Chart()
    chart.create('./performance/result/result.csv', 'value')
    #chart.create('./performance/result/result.csv', 'time')

if __name__ == '__main__':
    run()
