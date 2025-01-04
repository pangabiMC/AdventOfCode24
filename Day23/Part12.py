isTest = False
filename = "Day23/inputtest" if isTest else "Day23/input"

# init data
with open(filename) as file:
    Data = [line.strip() for line in file]

Connections = dict()
for d in Data:
    (c1, c2) = d.split('-') 
    Connections.setdefault(c1, set()).add(c2)
    Connections.setdefault(c2, set()).add(c1)

# Part1
# Naive brute force, fast enough
def generate_triangles(connections):
    visited = set()
    for curr in connections:
        loop_visited = set()
        for next in connections[curr]:
            if next in visited:
                continue
            for nextnext in connections[next]:
                if nextnext in visited or nextnext in loop_visited:
                    continue
                if curr in connections[nextnext]:
                    yield(curr, next, nextnext)
            loop_visited.add(next)
        visited.add(curr)

result = sum(1 for t in generate_triangles(Connections) if any(ti[0] == 't' for ti in t))
print(result)

# Part2
# using the Bron–Kerbosch algorithm
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bors_kerbosch_v1(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return 
    
    for v in P.union(set([])):
        bors_kerbosch_v1(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)

C = []
bors_kerbosch_v1(set([]), set(Connections.keys()), set([]), Connections, C)
c = max(sorted(C), key=len)
print(','.join(c))