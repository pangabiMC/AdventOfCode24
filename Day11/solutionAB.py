import numpy as np
filename = "Day11/inputtest"

with open(filename) as file:
    stones = list(map(int, file.read().strip().split()))
print(stones)

blink_target = 25

# part 1
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
blink_target = 50

def blink(stone) -> int:
    workset = {stone : 1}
    for count in range(0, blink_target):
        workset.popitem()


        for i in range(0, len(workset)):
            if workset[i] == 0:
                workset[i] = 1
            elif len(str(workset[i])) % 2 == 0:
                s = str(workset[i])
                workset[i] = int(s[:len(s)//2])
                workset.append(int(s[len(s)//2:]))
            else:
                workset[i] *= 2024
        print(count)
        print(len(workset))
    return len(workset)

print(sum(blink(stone) for stone in stones))

# blink_target = 50
# cache = {}
# def blink(stone) -> int:
#     workset = [(stone, blink_target)]
#     i = 0
#     while i < len(workset):
#         for count in range(0, workset[i][1]):
#             stone = workset[i][0]
#             if stone == 0:
#                 stone = 1
#             elif len(str(stone)) % 2 == 0:
#                 s = str(stone)
#                 stone = int(s[:len(s)//2])
#                 workset.append((int(s[len(s)//2:]), workset[i][1] - count - 1))
#             else:
#                 stone *= 2024
#             workset[i] = (stone, workset[i][1])
#         i += 1
#     return len(workset)

# print(sum(blink(stone) for stone in stones))