import re
import numpy as np
import itertools

isTest = True
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
# Ok this is stupid, but had to be done... more and more and more regex
# not sure if it would finish before the end of the universe
# (works charmingly for test input ofc)
# Compound pattern is a pattern that can be made of multiple smaller patterns
# Let's create all combinations of pattern sets with removing all compound patterns one at a time
# then do a regex search on all of the possible combinations
compoundPatterns = set()
for p in patterns:
    patternsExcept = patterns[:] # fast copy
    patternsExcept.remove(p)
    r = '^(' + '|'.join(patternsExcept) + ')+$'
    if re.match(r, p) is not None:
        compoundPatterns.add(p)

results = {}
print(f'total compound length = {len(compoundPatterns)}')
for L in range(1, len(compoundPatterns) + 1):
    for subset in itertools.combinations(compoundPatterns, L):
        patternsExcept = [p for p in patterns if p not in subset]
        m = '|'.join(patternsExcept)
        for d in designsMatching:
            match = re.findall(m, d)
            if match is not None:
                results.setdefault(d, set()).add(tuple(match))
result = 0
for m in results:
    result += len(results[m])

print(f'Part 2 Solution: {result}')
