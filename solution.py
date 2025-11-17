import random
from itertools import permutations

import numpy as np

Cn = 5
customers = list(range(1, Cn + 1))
print(customers)

customers = [0, 1, 2, 3, 4, 5]

customer_locations = {
    1: (35, 115),
    2: (50, 140),
    3: (70, 100),
    4: (40, 80),
    5: (25, 60),
}

items = {
    1: 1.2,
    2: 3.8,
    3: 7.5,
    4: 0.9,
    5: 15.4,
    6: 12.1,
    7: 4.3,
    8: 19.7,
    9: 8.6,
    10: 2.5
}

orders = {
    1: [{'item': 3, 'unit': 2}, {'item': 1, 'unit': 3}],
    2: [{'item': 2, 'unit': 6}],
    3: [{'item': 7, 'unit': 4}, {'item': 5, 'unit': 2}],
    4: [{'item': 3, 'unit': 8}],
    5: [{'item': 6, 'unit': 5}, {'item': 9, 'unit': 2}],
}


from itertools import permutations, product

import random

def random_list(max_length=10, min_val=0, max_val=5):
    length = random.randint(1, max_length)   # choose random length
    return [random.randint(min_val, max_val) for _ in range(length)]

lst = random_list()
print(lst)

population = [random_list() for x in range(100)]
print(population)
