import numpy as np

isTest = True
filename = "Day23/inputtest" if isTest else "Day23/input"


with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
