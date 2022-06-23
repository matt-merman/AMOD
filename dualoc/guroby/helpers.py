import random

def generate(max=1000):
    x = random.randint(0, max)
    return x

def populate_one(list, max):
    for i in range(max):
        x = generate()
        y = generate()
        list.append((x,y))
    return list

def populate_two(list, max):
    for i in range(max):
        x = generate()
        list.append(x)
    return list