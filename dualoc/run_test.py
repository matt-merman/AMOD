import performance.test as t

TRIAL = 500
NODE = 15
ALGORITHM = ['Dualoc', 'LP_relaxation', 'LP_lagrangian']
PATH = ['./performance/result.csv', './performance/mean_result.csv']

def run():

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

if __name__ == '__main__':
    run()