import pandas as pd

def create_list(path, attribute):

    df = pd.read_csv(path) 
    trial = df['#trial'].tolist()
    trial = list(set(trial))
    trial.sort()
    value = [[] for _ in range(0, len(trial))]

    index = 0
    for t in trial:
        for _, row in df.iterrows():
            if row['#trial'] == t:
                value[index].append(row[attribute])
        index += 1

    return value, trial