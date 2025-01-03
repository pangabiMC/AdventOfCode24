from functools import cache
from collections import deque
import time

isTest = False
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

def Part1Solution():
    result = 0
    for i in buyers:
        for _ in range(2000):  
            i = calc(i)
        result += i
    print(result)

Part1Solution()

# Part 2
# pretty much brute force, probably could be optimised, but solved it under 40 seconds, good enough
# We keep track of all price change sequences that occurs and store it if a monkey sells at that sequence
# There are not that many combination of possible sequences
start_time = time.time()
maxBuyers = len(buyers)
ledger = {}
sequenceLength = 4
# This will hold the last 4+1 secret numbers for all monkeys rolling as we iterate through the 2000 generations
# +1 because we need the extra to calc the diffs (this could be optimised so only the latest is kept, but hey ho)
secrets = deque([buyers.copy(), [0] * maxBuyers, [0] * maxBuyers, [0] * maxBuyers], sequenceLength + 1)

# for each iteration of secret numbers, calculates the current diffs and curr prices and updates the ledger
# we save all sequences of diffs in the ledger
def updateWins(secrets : deque, iteration: int):
    for i in range(maxBuyers):
        prices = [secrets[j][i] % 10 for j in range(sequenceLength + 1)] # the last digits of each kept secret numbers for this monkey
        sequence = tuple(j-i for i, j in zip(prices[1:], prices[:-1])) # the sequence of diffs
        currPrice = prices[0]
        if iteration >= sequenceLength - 1: # if we have enough entries already
            if sequence not in ledger:
                ledger[sequence] = [set(), 0] # for each sequence we keep track which monkey has had it and the total accumulated bananas we have for that sequence

            if i in ledger[sequence][0]: # this monkey has already sold for this sequence, should ignore it
                continue
            else: # this monkey would sell for this sequence (this is the first time for it) and we record the bananas we get from this monkey
                ledger[sequence][0].add(i)
                ledger[sequence][1] += currPrice

# now we do all the iteration for all the monkeys at once
for c in range(2000):
    secrets.appendleft(list((calc(secret) for secret in secrets[0])))
    updateWins(secrets, c)

# finally get the max value of bananas from the ledger (technically the key (ie the sequence) is not needed for the puzzle)
v = list(p[1] for p in ledger.values())
k = list(ledger.keys())
maxbananas = max(v)
print(f'{maxbananas} - {k[v.index(maxbananas)]}')
print("--- %s seconds ---" % (time.time() - start_time))