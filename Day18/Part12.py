import time

isTest = False

filename = "Day18/inputtest" if isTest else "Day18/input"
width = 7 if isTest else 71
height = 7 if isTest else 71
part1_split = 12 if isTest else 1024

with open(filename) as file:
    corrupted = [tuple(int(i) for i in line.strip().split(',')) for line in file]

# Part 1
# A* again, nothing spectacular, just plain path finding

# heuristic for A*, simple manhattan distance will do here
def h(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

# gets the move cost for this step including the turning if needed
def move_cost(curr, next):
    return 1

# gets all valid neighbours for a given node in the map
def get_neighbours(curr, corrupted, width, height):
    neighbours = []
    for neighbour in [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]), (curr[0], curr[1]-1), (curr[0], curr[1]+1)]:
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= height or neighbour[1] >= width or neighbour in corrupted:
            continue
        neighbours.append(neighbour)
    return neighbours

def get_min(from_set : set, priority: dict):
    current = None
    currentF = None
    for pos in from_set:
        if current is None or priority[pos] < currentF:
            currentF = priority[pos]
            current = pos
    return current

def A_star_search(start, end, corrupted):
    g = {}
    f = {}

    g[start] = 0
    f[start] = h(start, end)

    closed = set()
    open = set([start])
    came_from = {}

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

        for neighbour in get_neighbours(current, corrupted, width, height):
            if neighbour in closed:
                continue

            newG = g[current] + move_cost(current, neighbour)
            if neighbour not in open:
                open.add(neighbour)
            elif newG >= g[neighbour]:
                continue
            
            came_from[neighbour] = current
            g[neighbour] = newG
            f[neighbour] = newG + h(neighbour, end)

    return None

(path, cost) = A_star_search((0, 0), (width - 1, height - 1), corrupted[:part1_split])
print(f'Part 1 Solution: {cost}')

# part 2
# Perhaps there are quicker solutions, we do A* until we find the first that doesn't return a path
# the only optimisation here is that a block can only happen on a path, so we can skip ahead with the 
# iterations where the new corrupted block is not on the shortest path
# Finishes under 5 seconds
start_time = time.time()

foundPath = True
iteration = part1_split
while foundPath is not None:
    foundPath = A_star_search((0, 0), (width - 1, height - 1), corrupted[:iteration])
    if foundPath is not None:
        path_nodes = set(p[0] for p in foundPath[0])
        while corrupted[iteration - 1] not in path_nodes:
            iteration += 1
        print(iteration, end='\r')

print(f'Part 2 Solution: {corrupted[iteration-1]}')

print("--- %s seconds ---" % (time.time() - start_time))
 