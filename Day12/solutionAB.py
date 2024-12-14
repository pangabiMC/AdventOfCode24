import numpy as np
from itertools import product

filename = "Day12/input"

with open(filename) as file:
    matr = np.array([list(line.strip()) for line in file])
length = len(matr[0])

# part 1
def calculatePlot(x, y) -> tuple[set, int]:
    plant = matr[x][y]
    plot = set()
    expanded = {(x, y)}
    perimeter = 0
    while len(expanded) > 0:
        plot.update(expanded)
        curr_workset = expanded.copy()
        expanded = set()
        for (x, y) in curr_workset:
            for (newx, newy) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if newx in range(0, length) and newy in range(0, length) and matr[newx][newy] == plant and not (newx, newy) in plot:
                    expanded.add((newx, newy))
                elif not (newx, newy) in plot:
                    perimeter += 1

    return (plot, perimeter)

processed = set()
result = 0
not_processed = set(product(range(length), range(length)))
while len(not_processed) > 0:
    next_plot = not_processed.pop()
    (plot, perimeter) = calculatePlot(next_plot[0], next_plot[1])
    processed.update(plot)
    not_processed -= plot
    result += len(plot) * perimeter

print(result)
# part 2
