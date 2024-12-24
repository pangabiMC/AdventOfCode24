import numpy as np
from dataclasses import dataclass
import itertools
import time
import operator

isTest = True
filename = "Day20/inputtest" if isTest else "Day20/input"
minCost = 1 if isTest else 100

with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
width = len(map[0])
height = len(map)
start = list(zip(*np.where(map == 'S')))[0]
end = list(zip(*np.where(map == 'E')))[0]

# gets all valid neighbours for a given node in the map
# valid if within the map and is not a wall '#'
def getNext(prev, curr, map, width, height):
    n = []
    for neighbour in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
        if prev == neighbour or neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or map[neighbour] == '#':
            continue
        n.append(neighbour)
    return n

# just some convenience printing for debug
def printPath(map, path):
    for step in path:
        map[step] = 'o'
    for r in map:
        print(''.join(r))

@dataclass(eq=True, frozen=True)
class Cheat:
    start: tuple
    end: tuple
    saving: int

def getPathWithCosts(map, start, end):
    cost = 1
    path = {}
    path[start] = 0
    prev = None
    curr = start
    while curr != end:
        next = getNext(prev, curr, map, width, height)[0]
        path[next] = cost
        prev = curr
        curr = next
        cost += 1
    return path

def getCheats(costs, length = 2, mincost = 1):
    cheats = set()
    for curr in costs:
        for neighbour in [(curr[0]-length, curr[1]), (curr[0]+length, curr[1]), (curr[0], curr[1]-length), (curr[0], curr[1]+length)]:
            if neighbour in costs and costs[neighbour] - mincost >= costs[curr] + length:
                cheats.add(Cheat(curr, neighbour, costs[neighbour] - costs[curr] - length))
    return cheats

p = getPathWithCosts(map, start, end)
c = list(getCheats(p, mincost=minCost))
# c.sort(key=operator.attrgetter('saving'))
# for ch in c:
#     print(ch)
print(f'Part1: {len(c)}')
    
