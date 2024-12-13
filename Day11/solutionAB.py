filename = "Day11/input"

with open(filename) as file:
    stones = list(map(int, file.read().strip().split()))
print(stones)

blink_target = 25

# part 1
# Easy solution is recursive again... but this won't scale well
def blink(stone, count) -> int:
    if count == blink_target:
        return 1
    
    if stone == 0:
        return blink(1, count + 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        return blink(int(s[:len(s)//2]), count + 1) + blink(int(s[len(s)//2:]), count + 1)
    else:
        return blink(stone * 2024, count + 1)

print(sum(blink(stone, 0) for stone in stones))

# part 2
# Iterative solution is needed here, as well as some packing of the data
# Observation: when the list gets large there are many items that are the same. 
# We can group these into a dictionary and calculate the next stone for them at once
# So instead of a list of stones, we are working on a dictionary, each key is a stone value and its value is the 
# number of times that stone value appears.
blink_target = 75

def blink(stones) -> int:
    workset = {}
    for stone in stones:
        workset[stone] = 1 # all stone value is different in the input, otherwise we would need to set this up by counting them
    for count in range(0, blink_target): # we do the blinking steps on all stones at once
        nextset = {} # on each blink we collect the new set of values in a new dictionary
        while len(workset) > 0: 
            (stone, count) = workset.popitem() # so lets take each stone in the current set and do the math
            if stone == 0:
                stone = 1
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                stone = int(s[:len(s)//2])
                new_stone = int(s[len(s)//2:])
                nextset[new_stone] = nextset.get(new_stone, 0) + count
            else:
                stone *= 2024
            nextset[stone] = nextset.get(stone, 0) + count # create the new set by adding the new value, with the count the previous stone had
        workset = nextset.copy()
    return sum(workset.values())

print(blink(stones))