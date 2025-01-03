import numpy as np
from collections import deque

isTest = True
filename = "Day23/inputtest" if isTest else "Day23/input"

# init data
with open(filename) as file:
    data = [line.strip() for line in file]

connections = dict()
tmachines = set()
for d in data:
    (c1, c2) = d.split('-') 
    connections.setdefault(c1, set()).add(c2)
    connections.setdefault(c2, set()).add(c1)
    if c1[0] == 't':
        tmachines.add(c1)
    if c2[0] == 't':
        tmachines.add(c2)

nodes = list(connections)
# adj = [[0] * len(nodes) for _ in range(len(nodes))]
# for i in range(len(nodes)):
#     for c in connections[nodes[i]]:
#         adj[i][nodes.index(c)] = 1

# def printAdjMatr(adj, nodes):
#     print('   ' + ' '.join(nodes))
#     for n in nodes:
#         print(f"{n} {'  '.join(list(map(str, adj[nodes.index(n)])))}")

# print('\r\n\r\n')
# printAdjMatr(adj, nodes)

# adj3 = np.linalg.matrix_power(adj, 3)
# tlist = [n for n in nodes if n in tmachines]

# result = 0
# for i in range(len(tlist)):
#     t = tlist[i]
#     print(f'{t} - {adj3[nodes.index(t)][nodes.index(t)]}')
#     result += adj3[nodes.index(t)][nodes.index(t)] // 2 - sum(adj[nodes.index(t)][nodes.index(t0)] for t0 in tlist[i+1:])

# print(result)

# def getNthNeighbour(node: str, n: int) -> set:
#     if n == 1:
#         return set(connections[node])
#     s = set()
#     for nn in connections[node]:
#         s |= getNthNeighbour(nn, n - 1)
#     return s

# print(getNthNeighbour('td', 3))

# def search(current: str, visited: set, depth: int):
#     for n in connections[current]:
#         if n not in visited:
#             getNthNeighbour(n, 2)

# def bfs(node:str, maxDepth = 3):
#     q = deque([node])
#     paths = {node : []}
#     while q:
#         curr = q.popleft()
#         if len(paths[curr]) == maxDepth:
#             break
#         for n in connections[curr]:
#             if n not in paths:
#                 paths[n] = paths[curr] + [n]
#                 q.append(n)
#     return paths

# print(bfs('td'))

def generate_triangles(nodes):
    visited = set()
    for curr in nodes:
        loop_visited = set()
        for next in nodes[curr]:
            if next in visited:
                continue
            for nextnext in nodes[next]:
                if nextnext in visited or nextnext in loop_visited:
                    continue
                if curr in nodes[nextnext]:
                    yield(curr, next, nextnext)
            loop_visited.add(next)
        visited.add(curr)

result = 0        
for t in generate_triangles(connections):
    if any(ti[0] == 't' for ti in t):
        result += 1
print(result)