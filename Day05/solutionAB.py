from functools import cmp_to_key
filename = "Day05/input"

with open(filename) as file:
    data = [line.strip() for line in file]

# part 1 
beforeDict = {} # dictionary of sets -- key: number on left, value is set of all numbers on right
afterDict = {} # same but in reverse for reverse lookup
updates = []
for l in data:
    rule = l.split('|')
    if len(rule) == 2:
        beforeDict.setdefault(rule[0], set()).add(rule[1]) # creates the set if doesn't exist before adding the value
        afterDict.setdefault(rule[1], set()).add(rule[0])
    elif l:
        updates.append([i for i in l.split(',')])

def compare(item1, item2):
    if item1 in beforeDict and item2 in beforeDict[item1]:
        return -1
    elif item1 in afterDict and item2 in afterDict[item1]:
        return 1
    else:
        return 0

print(sum(int(update[(len(update) - 1)//2]) for update in updates if update == sorted(update, key=cmp_to_key(compare))))

# part 2 - lucky the sorting is already done in part 1
# this could be written in one line but becomes unreadable, but basically the same as above with a twist
result = 0
for update in updates:
    sorted_update = sorted(update, key=cmp_to_key(compare))
    if update != sorted_update:
        result += int(sorted_update[(len(sorted_update) - 1 )// 2])
print(result)
