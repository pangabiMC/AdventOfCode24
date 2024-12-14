import numpy as np
filename = "Day10/input"

with open(filename) as file:
    matr = np.array([list(map(int, line.strip())) for line in file])
length = len(matr[0])

start_points = np.array([*zip(*np.where(matr == 0))])

#part 1
# Recursion time. It's fine, we know it can't be deeper than 10.
# Stop recursion when reached 9 by returning the location of that trail end.
# On each step we step in all possible 4 direction, if its value is one higher than the current
# and append the trailend location found in that direction
def getTrailEnd(x, y):
    curr = matr[x][y]
    if curr == 9:
        return [(x, y)]
    ret = []
    for (newx, newy) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if newx in range(0, length) and newy in range(0, length) and matr[newx][newy] == curr + 1:
            ret += getTrailEnd(newx, newy)
    return ret

# convert the list of 9 positions found to a set to get the unique trail ends found
print(sum(len(set(getTrailEnd(s[0], s[1]))) for s in start_points))

#part 2
# This was so satisfying. The recusrion will have already walked all possible routes, so we just count the number of times it reached the trail end
print(sum(len(getTrailEnd(s[0], s[1])) for s in start_points))
