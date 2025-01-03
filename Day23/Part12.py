import numpy as np

isTest = True
filename = "Day23/inputtest" if isTest else "Day23/input"

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

for t in tmachines:
    print(f'{t} - {connections[t]}')

nodes = list(connections)
adj = [[0] * len(nodes) for _ in range(len(nodes))]
for i in range(len(nodes)):
    for c in connections[nodes[i]]:
        adj[i][nodes.index(c)] = 1

adj3 = np.linalg.matrix_power(adj, 3)
tlist = [n for n in nodes if n in tmachines]

result = 0
for i in range(len(tlist)):
    t = tlist[i]
    print(f'{t} - {adj3[nodes.index(t)][nodes.index(t)]}')
    result += adj3[nodes.index(t)][nodes.index(t)] // 2 - sum(adj[nodes.index(t)][nodes.index(t0)] for t0 in tlist[i+1:])

print(result)

def printAdjMatr(adj, nodes):
    print('   ' + ' '.join(nodes))
    for n in nodes:
        print(f"{n} {'  '.join(list(map(str, adj[nodes.index(n)])))}")

printAdjMatr(adj, nodes)

def getNthNeighbour(node: str, n: int) -> set:
    if n == 1:
        return set(connections[node])
    s = set()
    for nn in connections[node]:
        s |= getNthNeighbour(nn, n - 1)
    return s

print(getNthNeighbour('td', 3))

def search(current: str, visited: set, depth: int):
    for n in connections[current]:
        if n not in visited:
            getNthNeighbour(n, 2)

