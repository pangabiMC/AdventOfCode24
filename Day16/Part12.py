import numpy as np
import itertools
import time

filename = "Day16/input"

with open(filename) as file:
    map = np.array([list(line.strip()) for line in file])
width = len(map[0])
height = len(map)

# Part1 is a simple pathfinding, the only interesting bit is that the move cost will take the turns into account:
# comparing where we came from and where we are heading, we can tell if the step needs a turn
# so for each move cost we need not just the neighbour and the current node, but the previous node as well

# heuristic for A*, simple manhattan distance will do here
def h(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

# gets the move cost for this step including the turning if needed
def move_cost(prev, curr, next):
    if curr[0] - prev[0] == next[0] - curr[0] and curr[1] - prev[1] == next[1] - curr[1]: # we are not changing direction
        cost = 1
    else: 
        cost = 1001
    return cost

# gets all valid neighbours for a given node in the map
# valid if within the map and is not a wall '#'
def get_neighbours(curr, map, width, height):
    n = []
    for neighbour in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or map[neighbour] == '#':
            continue
        n.append(neighbour)
    return n

def get_min(from_set : set, priority: dict):
    current = None
    currentF = None
    for pos in from_set:
        if current is None or priority[pos] < currentF:
            currentF = priority[pos]
            current = pos
    return current

# Only extra here is that we need the previous node for the start to know if we do a turn on step 1
# as in the puzzle description: we start from the west, but for Part 2 we will need to pass this in
# Also for Part 2 we need to return each cost value for each node in the final path
def A_star_search(start_prev, start, end, map):
    g = {}
    f = {}

    g[start] = 0
    f[start] = h(start, end)

    closed = set()
    open = set([start])
    came_from = {}
    came_from[start] = start_prev

    while len(open) > 0:
        current = get_min(open, f)
        
        if current == end:
            path = [(current, g[current])]
            while current in came_from:
                current = came_from[current]
                path.append((current, g[current] if current in g else 0))
            return path, f[end]
        
        open.remove(current)
        closed.add(current)

        for neighbour in get_neighbours(current, map, width, height):
            if neighbour in closed:
                continue

            newG = g[current] + move_cost(came_from[current], current, neighbour)
            if neighbour not in open:
                open.add(neighbour)
            elif newG >= g[neighbour]:
                continue
            
            came_from[neighbour] = current
            g[neighbour] = newG
            f[neighbour] = newG + h(neighbour, end)

    return None

# just some convenience printing for debug
def printPath(map, path):
    for step in path:
        map[step] = 'o'
    for r in map:
        print(''.join(r))

# get the start and end from the map
start = list(zip(*np.where(map == 'S')))[0]
end = list(zip(*np.where(map == 'E')))[0]
start_prev = (start[0], start[1]-1)

start_time = time.time()
# and that's the solution
(path, cost) = A_star_search(start_prev, start, end, map)

#print(path)
#printPath(map.copy(), list((node for (node, c) in path)))
print(f'Soution: {cost}')
print("--- %s seconds ---" % (time.time() - start_time))

# Part 2:
# Probably not the best idea, but worked... and took "only" 11 seconds
# I couldn't figure out how to get all shortest path in one run using Dijkstra or A*. 
# (because all costs depends on where we came from, so a node cost might be higher on a 2nd path, but the next node is equal)
# DFS worked for test but wasn't scaling well to real input. (even if added the max cost limit to terminate wrong paths early)
# So:
# We start by the path and cost found by A*
# Then walk back on it and at each point there is a possible neighbour we didn't yet investigate (ie it's a junction in the maze)
# We run another A* back to start from that junction (could have been fwd too), but now the winner path blocked with a temporary '#'
# If the A* finds an alternative path from that junction, then compare its length to the known lowest cost. If == then we have an alternative path.
# BUT
# Then this alternative path might spawn other alternative paths in junctions alongside this new path.
# So we have to do this A* backtrace in a recursive manner (could be converted to iterative)
paths = []
paths.append(path)

def find_alternative_paths(path, paths, end):
    for i in range(0, len(path)-1): # we walk backwards on the shortest path
        curr = path[i][0]
        prev = path[i-1][0] if i > 0 else end

        for n in get_neighbours(curr, map, width, height): 
            if (i < 1 or n != path[i-1][0]) and n != path[i+1][0]: # if we have a neighbour that's not wall and not on the shortest path already then we try to run a new path from here
                map[curr] = '#' # close the already shortest path
                alt_path = A_star_search(start_prev, start, n, map) # and run a new search from the maze start till the neighbour
                map[curr] = '.'
                if alt_path != None and alt_path[1] + move_cost(prev, curr, n) <= path[i-1][1]:
                    paths.append(alt_path[0])
                    find_alternative_paths(alt_path[0], paths, prev) # do this with the new alternative paths too
start_time = time.time()
find_alternative_paths(path, paths, end)
result = len(set(node for (node, c) in itertools.chain.from_iterable(paths)))
print(f'Soution: {result-1}')
print("--- %s seconds ---" % (time.time() - start_time))

#printPath(map, list((node for (node, c) in itertools.chain.from_iterable(paths))))
