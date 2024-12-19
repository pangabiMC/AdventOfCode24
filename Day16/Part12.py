import numpy as np

filename = "Day16/input"

with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
width = len(map[0])
height = len(map)

def h(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def move_cost(prev, curr, next):
    if curr[0] - prev[0] == next[0] - curr[0] and curr[1] - prev[1] == next[1] - curr[1]: # we are not changing direction
        cost = 1
    else: 
        cost = 1001
    return cost

def A_star_search(start, end, map):
    g = {}
    f = {}

    g[start] = 0
    f[start] = h(start, end)

    closed = set()
    open = set([start])
    came_from = {}
    came_from[start] = (start[0], start[1]-1)

    while len(open) > 0:
        current = None
        currentF = None
        for pos in open:
            if current is None or f[pos] < currentF:
                currentF = f[pos]
                current = pos
        
        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, f[end]
        
        open.remove(current)
        closed.add(current)

        for neighbour in [(current[0]-1, current[1]), (current[0]+1, current[1]), (current[0], current[1]-1), (current[0], current[1]+1)]:
            if neighbour in closed:
                continue
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or map[neighbour] == '#':
                continue

            newG = g[current] + move_cost(came_from[current], current, neighbour)
            if neighbour not in open:
                open.add(neighbour)
            elif newG >= g[neighbour]:
                continue
            
            came_from[neighbour] = current
            g[neighbour] = newG
            f[neighbour] = newG + h(neighbour, end)

    raise RuntimeError("A* failed to find a solution")

def printPath(map, path):
    for step in path:
        map[step] = 'X'
    for r in map:
        print(''.join(r))

start = list(zip(*np.where(map == 'S')))[0]
end = list(zip(*np.where(map == 'E')))[0]

(path, cost) = A_star_search(start, end, map)

print(path)
print(cost)
printPath(map.copy(), path)