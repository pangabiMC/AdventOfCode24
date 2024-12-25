import numpy as np
import itertools

isTest = False
filename = "Day25/inputtest" if isTest else "Day25/input"

with open(filename) as file:
    data = np.array([list(line.strip()) for line in file if len(line.strip()) > 0])

keys = []
locks = []

for i in range(0, len(data), 7):
    k = np.array([np.count_nonzero(data[i+1:i+6][:,j] == '#') for j in range(5)])
    if data[i][0] == '#':
        locks.append(k)
    else:
        keys.append(k)

result = sum(1 for t in itertools.product(keys, locks) if np.all((t[0] + t[1]) < 6))
print(result)


