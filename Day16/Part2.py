import numpy as np
import itertools

filename = "Day16/input"

with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
width = len(map[0])
height = len(map)

def h(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def move_cost(prev, curr, next):
    if prev == curr:
        cost = 0
    elif curr[0] - prev[0] == next[0] - curr[0] and curr[1] - prev[1] == next[1] - curr[1]: # we are not changing direction
        cost = 1
    else: 
        cost = 1001
    return cost

def get_min(from_set : set, priority: dict):
    current = None
    currentF = None
    for pos in from_set:
        if current is None or priority[pos] < currentF:
            currentF = priority[pos]
            current = pos
    return current

def get_neighbours(curr, map, width, height):
    n = []
    for neighbour in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or map[neighbour] == '#':
            continue
        n.append(neighbour)
    return n

def A_star_search(first_prev, start, end, map):
    g = {}
    f = {}

    g[start] = 0
    f[start] = h(start, end)

    open = set([start])
    came_from = {}
    came_from[start] = first_prev

    while len(open) > 0:
        current = get_min(open, f)
        
        if current == end:
            path = [(current, g[current])]
            while current in came_from:
                current = came_from[current]
                path.append((current, g[current] if current in g else 0))
            return path, f[end]
        
        open.remove(current)

        for neighbour in get_neighbours(current, map, width, height):
            newG = g[current] + move_cost(came_from[current], current, neighbour)
            if neighbour not in g.keys() or newG < g[neighbour]:
                if neighbour not in open:
                    open.add(neighbour)
                came_from[neighbour] = current
                g[neighbour] = newG
                f[neighbour] = newG + h(neighbour, end)

    return None

def printPath(map, path):
    for step in path:
        map[step] = 'o'
    for r in map:
        print(''.join(r))

def printCurr(map, curr, next):
    map[curr] = 'o'
    map[next] = 'n'
    for r in map:
        print(''.join(r))

def printCameFrom(map, path):
    for step in path:
        if len(path[step]) > 0:
            map[step] = 'o'
    for r in map:
        print(''.join(r))

def get_all_paths(map, came_from, v):
    s = list([v])
    processed = set()
    while len(s) > 0:
        v = s.pop()
        #if v not in processed:
        processed.add(v)
        for prev in came_from[v]:
            s.append(prev)
    printPath(map.copy(), processed)


start = list(zip(*np.where(map == 'S')))[0]
end = list(zip(*np.where(map == 'E')))[0]
start_prev = (start[0], start[1]-1)

paths = []

(path, cost) = A_star_search(start_prev, start, end, map)
paths.append(path)

def find_alternative_paths(path, paths, end):
    for i in range(0, len(path)-1):
        curr = path[i][0]
        prev = path[i-1][0] if i > 0 else end
        for n in get_neighbours(curr, map, width, height):
            if (i < 1 or n != path[i-1][0]) and n != path[i+1][0]:
                m = map.copy()
                m[curr] = '#'
                alt_path = A_star_search(start_prev, start, n, m)
                if alt_path != None and alt_path[1] + move_cost(prev, curr, n) <= path[i-1][1]:
                    paths.append(alt_path[0])
                    find_alternative_paths(alt_path[0], paths, prev)

find_alternative_paths(path, paths, end)

result = len(set(node for (node, c) in itertools.chain.from_iterable(paths)))
printPath(map, list((node for (node, c) in itertools.chain.from_iterable(paths))))
print(result-1)