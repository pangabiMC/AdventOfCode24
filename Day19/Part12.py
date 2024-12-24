import re
from functools import cache

isTest = False
filename = "Day19/inputtest" if isTest else "Day19/input"
with open(filename) as file:
    lines = [line.strip() for line in file]
patterns = [l.strip() for l in lines[0].split(',')]
designs = lines[2:]

# Part 1
# let the regex engine do the job
patterns.sort(key=len, reverse=True) # for regex to work correctly here we need to sort the patterns from longest to shortest
megabrutalregexpattern = '^(' + '|'.join(patterns) + ')+$'
designsMatching = [d for d in designs if re.match(megabrutalregexpattern, d) is not None]
print(f'Part 1 Solution: {len(designsMatching)}')

# Part 2
# simple pattern search recursively, to optimise we only check the valid designs from Part 1
# still, this takes ages without memoization... 
# lucky python has its own solution to that
@cache
def doMatch(design : str) -> int:
    if len(design) == 0:
        return 1
    return sum(doMatch(design[len(p):]) for p in patterns if design.startswith(p))

result = sum(doMatch(d) for d in designsMatching)
print(f'Part 2 Solution: {result}')
