import numpy as np
from dataclasses import dataclass

isTest = False
filename = "Day20/inputtest" if isTest else "Day20/input"
minCost = 1 if isTest else 100

with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
width = len(map[0])
height = len(map)
start = list(zip(*np.where(map == 'S')))[0]
end = list(zip(*np.where(map == 'E')))[0]

# Part 1 and 2
# The puzzle description is not the clearest, but luckly the the simplest possible is the correct one.
# We first calculate the cost of all nodes (how many steps they are from the Start)
# Then we try every node for all possible cheats...
# for part 1 this is fast, for part 2 there must be more optimal solutions but this is still < 10 seconds, so it will do
# Checking for cheat is simply taking all neighbours for the allowed distance
# if the neighbour is also on the path, then check how much we could save if that neighbour was the next step (plus the cheat length)


@dataclass(eq=True, frozen=True)
class Cheat:
    start: tuple
    end: tuple
    saving: int

# gets all valid neighbours for a given node in the map
# valid if within the map and is not a wall '#'
def getNext(prev, curr, map, width, height):
    return [n for n in [
        (curr[0]-1, curr[1]), 
        (curr[0]+1, curr[1]), 
        (curr[0], curr[1]-1), 
        (curr[0], curr[1]+1)] if (prev != n and
         n[0] in range(0, height) and n[1] in range(0, width) and map[n] != '#')]
         
# gets the list of nodes that are on the path from start to finish, each with their "cost" ie steps from start
def getPathWithCosts(map, start, end):
    cost = 1
    path = { start: 0 }
    prev = None
    curr = start
    while curr != end:
        next = getNext(prev, curr, map, width, height)[0]
        path[next] = cost
        prev = curr
        curr = next
        cost += 1
    return path

# gets the coordinates (regardless if valid) of all neighbours of current reachable from current within maximum N step
def getNthNeighbours(curr, n) -> list:
    return [(x,y) for x in range(curr[0]-n, curr[0]+n+1) for y in range(curr[1]-(n-abs(curr[0]-x)), curr[1]+n-abs(curr[0]-x)+1)]

# gets all cheats that allows 'length' amount of going through the wall and that saves at least mincost amount
def getCheats(costs, length, mincost):
    cheats = set()
    for curr in costs:
        for neighbour in getNthNeighbours(curr, length):
            stepsToNeighbour = abs(neighbour[0] - curr[0]) + abs(neighbour[1] - curr[1])
            if neighbour in costs and costs[neighbour] - mincost >= costs[curr] + stepsToNeighbour:
                cheats.add(Cheat(curr, neighbour, costs[neighbour] - costs[curr] - stepsToNeighbour))
    return cheats

# Part 1
path = getPathWithCosts(map, start, end)
allCheats = list(getCheats(path, 2, minCost))
print(f'Part1: {len(allCheats)}')

# Part 2
minCost = 50 if isTest else 100
allCheats = list(getCheats(path, 20, minCost))
print(f'Part2: {len(allCheats)}')

    
