import pandas as pd
import numpy as np


def create_list(path, attribute, algorithm_list):

    df = pd.read_csv(path)
    facility = df['#facility'].tolist()
    facility = list(set(facility))
    facility.sort()

    customer = df['#customer'].tolist()
    customer = list(set(customer))

    value = [[] for _ in range(0, len(facility))]

    index = 0
    for t in facility:
        for _, row in df.iterrows():
            if row['#facility'] == t and row['algorithm'] in algorithm_list:
                value[index].append(row[attribute])
        index += 1

    return value, facility, customer


def create_multiplier(f, c):
    dic = {}
    for i in range(f):
        for j in range(c):
            key = (j, i)
            value = np.random.randint(1, 100)
            dic[key] = value
    return dic

# Percent Error = |Experimental Value – Theoretical Value|/|Theoretical value| × 100


def percent_error(experimental_value, theoretical_value):
    n = abs(experimental_value - theoretical_value)
    d = abs(theoretical_value)
    return (n/d) * 100
