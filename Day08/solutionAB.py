import numpy as np
from itertools import combinations
import math 

filename = "Day08/input"

with open(filename) as file:
    matr = np.array([list(line.strip()) for line in file])
length = len(matr[0])

# part 1

antinodes = []
frequencies = set(matr.flatten()) # each character other than . is a separate frequency
frequencies.remove('.')
for f in frequencies:
    antennas = np.array([*zip(*np.where(matr == f))]) # only looking at the antennas for this frequency
    for (a1, a2) in combinations(antennas, 2): # gets all possible pairs within the array
        antinodes.append(a1 - (a2 - a1))
        antinodes.append(a2 + (a2 - a1))
antinodes = np.unique(antinodes, axis=0) # remove the overlapping antinodes
result = sum(1 for a in antinodes if a[0] in range(0, length) and a[1] in range(0, length)) # count those that are within the map
print(result)

# part 2
# same as part 1 but we add the difference vector as many times as possible - this will also cover the antennas as they should
antinodes = []
for f in frequencies:
    antennas = np.array([*zip(*np.where(matr == f))])
    for (a1, a2) in combinations(antennas, 2):
        diff = a2 - a1
        dist = math.dist(a2, a1)
        for i in range(0, math.ceil(length / dist) + 1):
            antinodes.append(a1 - i * (a2 - a1))
            antinodes.append(a2 + i * (a2 - a1))
antinodes = np.unique(antinodes, axis=0)
result = sum(1 for a in antinodes if a[0] in range(0, length) and a[1] in range(0, length))
print(result)
