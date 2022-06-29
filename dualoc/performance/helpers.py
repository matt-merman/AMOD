import pandas as pd
import numpy as np

def create_list(path, attribute):

    df = pd.read_csv(path)
    facility = df['#facility'].tolist()
    facility = list(set(facility))
    facility.sort()
    value = [[] for _ in range(0, len(facility))]

    index = 0
    for t in facility:
        for _, row in df.iterrows():
            if row['#facility'] == t:
                value[index].append(row[attribute])
        index += 1

    return value, facility


def create_multiplier(f, c):
    dict = {}
    for i in range(f):
        for j in range(c):
            key = (j, i)
            value = np.random.randint(1, 1000)
            dict[key] = value
    return dict
