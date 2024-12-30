import numpy as np
from functools import cache

isTest = True
filename = "Day22/inputtest" if isTest else "Day22/input"


with open(filename) as file:
    data = [int(line.strip()) for line in file]


# Part 1 - the naive solution aka brute force
@cache
def calc(i: int) -> int:
    i ^= i << 6
    i &= (2 ** 24 - 1)
    i ^= i >> 5
    i &= (2 ** 24 - 1)
    i ^= i << 11
    i &= (2 ** 24 - 1)
    return i

result = 0
for i in data:
    for c in range(2000):  
        i = calc(i)
    result += i

print(result)


# Part 2
