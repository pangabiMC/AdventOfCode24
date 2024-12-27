import numpy as np

isTest = True
filename = "Day22/inputtest" if isTest else "Day22/input"


with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
