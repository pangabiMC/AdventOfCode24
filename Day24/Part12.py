import numpy as np

isTest = True
filename = "Day24/inputtest" if isTest else "Day24/input"


with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
