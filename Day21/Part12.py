import numpy as np

isTest = False
filename = "Day21/inputtest" if isTest else "Day21/input"


with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
