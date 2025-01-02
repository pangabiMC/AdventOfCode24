import numpy as np
from functools import cache

isTest = False
filename = "Day21/inputtest" if isTest else "Day21/input"

with open(filename) as file:
    data = [(line.strip()) for line in file]

# Part 1 and 2 ... the only difference is the number of robots at the end
# This took me a while... but finally running time is suprisingly superfast
# Key realisations: 
#  * moves can be horizontal first then vertical; or the other way round
#  * it's not obvious which will be shorter after N robot level
#  * so recursion should handle the forks
#  * caching will take care of the complexity
#  * each robot ends with A and starts a sequence from A
#  * we need the length of each key change on every robot level...
# Example:
# level 0: A6       -> Going from A to 6 we get the possible routes between the two
# level 1: (A)^^A   -> Only 1 route exists. Take all pairs (A< <A AA A> >A) and get the routes for each
# level 2: (A)<AA>A -> repeat recursively with all pairs

dirkeys = set('^<v>')
numpad = np.array([['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']])
dirpad = np.array([['X','^','A'],['<','v','>']])

# Gets if the character pair belong to the numpad or the directional pad 
# ('A' is shared on both, that's why we need a pair to be able to decide)
@cache
def isNumpad(start: chr, end: chr):
    return start not in dirkeys and end not in dirkeys

# Gets the possible routes in a form of direction sequence between the two characters 
# (whether its numpad or dirpad is determined from the characters)
# This discards routes which would go over the blank X key 
# It returns a tuple of sequences, the first element is always a route, the second may be None if only one route exists
@cache
def keys_to_moves(start: chr, end: chr) -> tuple:
    if isNumpad(start, end):
        s = list(zip(*np.where(numpad == start)))[0]
        e = list(zip(*np.where(numpad == end)))[0]
    else:
        s = list(zip(*np.where(dirpad == start)))[0]
        e = list(zip(*np.where(dirpad == end)))[0]
    
    diff = (e[0] - s[0], e[1] - s[1])

    horiz = '<' * abs(diff[1]) if diff[1] < 0 else '>' * diff[1]
    vert = '^' * abs(diff[0]) if diff[0] < 0 else 'v' * diff[0]

    # remove the duplicates (if the two routes would be the same)
    if diff[0] == 0 or diff[1] == 0:
        return (horiz + vert + 'A', None)
    
    # remove invalid routes (where we go over the gap on the pad)
    if isNumpad(start, end): 
        if s[1] == 0 and e[0] == 3:
            return(horiz + vert + 'A', None)
        elif s[0] == 3 and e[1] == 0:
            return(vert + horiz + 'A', None)
    elif start == '<': # keypad avoiding blank
        return(horiz + vert + 'A', None)
    elif end == '<': # keypad avoiding blank
        return(vert + horiz + 'A', None)
    
    return (horiz + vert + 'A', vert + horiz + 'A')

# Gets the number of moves on the i-th robot of going from one key to another
@cache
def cost(start: chr, end:chr, robot_i:int) -> int:
    if start is None:
        start = 'A'
    (r0, r1) = keys_to_moves(start, end)
    if robot_i == 0:
        return len(r0) # same as r[1]
    nextCost = cost_sequence(r0, robot_i-1)
    if r1 is not None:
        nextCost = min(nextCost, cost_sequence(r1, robot_i-1))
    return nextCost

# Gets the number 
@cache
def cost_sequence(seq: str, robot_i: int) -> int:
    return sum(cost(seq[i-1] if i != 0 else None, seq[i], robot_i) for i in range(len(seq)))

# Main
num_robots = 25 # 2 for Part 1 
r = sum(int(d[:-1]) * cost_sequence(d, num_robots) for d in data)
print(r)

