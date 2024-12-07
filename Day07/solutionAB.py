filename = "Day07/inputtest"

with open(filename) as file:
    lines = [line.strip() for line in file]

# part 1

def isValid(left, right) -> bool:
    if len(right) == 1:
        return left == right[0]
    return (left % right[-1] == 0 and isValid(left // right[-1], right[:-1])) or isValid(left - right[-1], right[:-1])

result = 0
for l in lines:
    left = int(l.split(':')[0])
    right = [int(i) for i in l.split(':')[1].split()]
    if isValid(left, right):
        result += left

print(result)

#part 2
def isValid2(left, right) -> bool:
    if len(right) == 0:
        return False
    if len(right) == 1:
        return left == right[0]
    concat = int(str(right[-2]) + str(right[-1]))
    return  ((left % right[-1] == 0 and isValid2(left // right[-1], right[:-1])) or 
              (left % concat == 0 and isValid2(left // concat, right[:-2])) or
            isValid2(left - right[-1], right[:-1]) 
            or isValid2(left, right[:-2] + [concat]))

result = 0
for l in lines:
    left = int(l.split(':')[0])
    right = [int(i) for i in l.split(':')[1].split()]
    if isValid2(left, right):
        result += left
print(result)