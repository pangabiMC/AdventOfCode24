import numpy as np
from functools import cache
from collections import deque

isTest = True
filename = "Day22/inputtest" if isTest else "Day22/input"


with open(filename) as file:
    buyers = [int(line.strip()) for line in file]


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

# result = 0
# for i in buyers:
#     for c in range(2000):  
#         i = calc(i)
#     result += i

# print(result)

# Part 2
maxBuyers = len(buyers)

def updateWins(prices : deque):
    for i in range(maxBuyers):
        sequence = None
    return None


prices = deque([buyers.copy(), [], [], []], 4)
for c in range(2000):
    prices.appendleft(list((calc(price) for price in prices[0])))
    if c >= 4:
        updateWins(prices)


print(prices)
