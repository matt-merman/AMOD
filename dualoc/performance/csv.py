import csv

class CSV:
    def __init__(self, file):
        self.file = file

    def create_csv(self):
        header = ['#trial', '#facility', '#customer', 'algorithm', 'value', 'time']
        f = open(self.file, 'w')
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    
    def add_row(self, trial, facility, customer, algorithm, value, time):
        list_data=[trial, facility, customer, algorithm, value, time]
        
        with open(self.file, 'a', newline='') as f_object:  
            writer_object = csv.writer(f_object)
            writer_object.writerow(list_data)  
            f_object.close()
   