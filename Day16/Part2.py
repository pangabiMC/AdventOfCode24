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

def dfs(start, end, map, limit):
    curr_path = []
    visited = set()
    paths = []

    def dfs_rec(prev : tuple, curr : tuple, end : tuple, curr_cost : int):
        if curr == end:
            if curr_cost == limit:
                paths.append([x for x in curr_path])
            return

        for n in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
            if n[0] < 0 or n[1] < 0 or n[0] >= height or n[1] >= width or map[n] == '#':
                continue
            if n in visited:
                continue
            cost = move_cost(prev, curr, n)
            if curr_cost + cost + h(n, end) <= limit:
                visited.add(n)
                curr_path.append(n)

                dfs_rec(curr, n, end, curr_cost + cost)
                
                curr_path.pop()
                visited.remove(n)

    dfs_rec((start[0], start[1]-1), start, end, 0)
    return paths



def dijkstra(start, end, map):
    dist = {}
    came_from = {}
    q = set()
    
    for v in [(i, j) for i in range(0, height) for j in range(0,width)]:
        q.add(v)
        dist[v] = float('inf')
        came_from[v] = set()
    
    came_from[start].add((start[0], start[1]-1))
    dist[start] = 0
    
    while len(q) > 0:
        curr = get_min(q, dist)
        
        # if curr == end:
        #     path = [curr]
        #     while curr in came_from:
        #         curr = came_from[curr]
        #         path.append(curr)
        #     path.reverse()
        #     return path, dist[end]

        q.remove(curr)

        if len(came_from[curr]) == 0:
            continue

        for n in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
            if n[0] < 0 or n[1] < 0 or n[0] >= height or n[1] >= width or map[n] == '#':
                continue
            printCurr(map.copy(), curr, n)
            newDist = min(dist[curr] + move_cost(prev, curr, n) for prev in came_from[curr])
            if n not in dist or newDist <= dist[n]:
                came_from[n].add(curr)
                dist[n] = newDist
                print(came_from[n])
                print(dist[n])

    return came_from


def A_star_search(start, end, map):
    g = {}
    f = {}

    g[start] = 0
    f[start] = h(start, end)

    open = set([start])
    came_from = {}
    came_from[start] = (start[0], start[1]-1)

    while len(open) > 0:
        current = get_min(open, f)
        
        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, f[end]
        
        open.remove(current)

        for neighbour in [(current[0]-1, current[1]), (current[0]+1, current[1]), (current[0], current[1]-1), (current[0], current[1]+1)]:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or map[neighbour] == '#':
                continue

            newG = g[current] + move_cost(came_from[current], current, neighbour)
            if neighbour not in g.keys() or newG < g[neighbour]:
                if neighbour not in open:
                    open.add(neighbour)
                came_from[neighbour] = current
                g[neighbour] = newG
                f[neighbour] = newG + h(neighbour, end)

    raise RuntimeError("A* failed to find a solution")

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

(path, cost) = A_star_search(start, end, map)
allPaths = dfs(start, end, map, cost)

print(allPaths)

merged = list(itertools.chain.from_iterable(allPaths))
printPath(map, merged)
print(len(list(zip(*np.where(map == 'o'))))+1)

#c = dijkstra(start, end, map)
#print(c)
#get_all_paths(map.copy(), c, end)

# (path, cost) = A_star_search(start, end, map)
# print(path)
# print(cost)
# printPath(map.copy(), path)