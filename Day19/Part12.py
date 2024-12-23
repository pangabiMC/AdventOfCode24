import time
import re

isTest = True

filename = "Day19/inputtest" if isTest else "Day19/input"

with open(filename) as file:
    lines = [line.strip() for line in file]

patterns = [l.strip() for l in lines[0].split(',')]
patterns.sort(key=len, reverse=True)
designs = lines[2:]
megabrutalregexpattern = '^(' + '|'.join(patterns) + ')+$'

# print(patterns)
# print(designs)
# print(megabrutalregexpattern)
result = sum(1 for d in designs if re.match(megabrutalregexpattern, d) is not None)
print(result)
