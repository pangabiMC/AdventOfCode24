import numpy as np
from itertools import product

filename = "Day12/input"
with open(filename) as file:
    matr = np.array([list(line.strip()) for line in file])
length = len(matr[0])

# Given a set of fences (a tuple of coordinates and a direction (both tuples, direction is (0,1) etc)) it counts the number of continuous sequences
# Take any fence from the set, then remove all adjacent fences by walking the 90 degree rotated direction up and down while the next fence is in the set
def number_of_sides(perimeter : list) -> int:
    sides = 0
    while len(perimeter) > 0:
        (fence, direction) = perimeter.pop()
        sides += 1
        for i in [1, -1]:   # to walk up and then down from the starting point
            next_fence_segment = fence
            while True:
                next_fence_segment = (next_fence_segment[0] + i * direction[1], next_fence_segment[1] + i * direction[0])
                if (next_fence_segment, direction) in perimeter:
                    perimeter.remove((next_fence_segment, direction))
                else:
                    break
    return sides

# From any starting point in the map it returns the entire enclosed plot for the plant on that starting coordinate, and all fences on the plot's perimeter
# We do this by expanding from each already discovered plot coordinates to all possible direction in a loop, until no new areas are discovered.
def calculatePlot(x, y, isPart2) -> tuple[set, int]:
    plant = matr[x][y]      # the plant (character) we are interested in for this run
    plot = set()            # this is where we collect the coordinates of the plot
    perimeter = set()       # this is where we collect the coordinates of the fence pieces and the direction they are facing
    expanded = {(x, y)}     # the set of new plot coordinates that we gathered in the last iteration
    while len(expanded) > 0:    # we try to expand until no new areas are found
        plot.update(expanded)   # bank in what we collected on the previous iteration
        curr_workset = expanded.copy()  # this is going to be our new workset to expand from
        expanded = set()    # and here we collect the next expansion
        for (x, y) in curr_workset:
            for (newx, newy) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]: # we will try to expand from each cell towards all 4 possible directions
                # if we are still on the map and the cell is the same plant (and not have been discovered already)
                if 0 <= newx < length and 0 <= newy < length and matr[newx][newy] == plant and not (newx, newy) in plot:
                    expanded.add((newx, newy)) # then expand
                elif not (newx, newy) in plot: # otherwise (if we're still on the map, but it's a different plant)
                    perimeter.add(((x, y), (newx - x, newy - y))) # then it's a fence
    p = len(perimeter) # Part 1 needs the number of fence cells
    if(isPart2):
        p = number_of_sides(perimeter) # Part 2 also calculates the number of continuous fence sequences
    return (plot, p)

# To solve we keep a list of all unprocessed (not in a plot yet) coordinates.
# Until this list is empty, we take the next starting point from it, and expand the plot.
def solve(isPart2: bool) -> int:
    processed = set()
    result = 0
    not_processed = list(product(range(length), range(length)))
    while len(not_processed) > 0:
        next_plot = not_processed[0]
        (plot, perimeter) = calculatePlot(next_plot[0], next_plot[1], isPart2)
        processed.update(plot)
        for i in plot:
            if i in not_processed:
                not_processed.remove(i)
        result += len(plot) * perimeter
    return result

print(solve(False))
print(solve(True))
