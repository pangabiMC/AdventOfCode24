filename = "Day07/input"

input = []
with open(filename) as file:
    for l in [line.strip() for line in file]:
        input.append((int(l.split(':')[0]), [int(i) for i in l.split(':')[1].split()]))

# part 1

# let's do some recursion here - we can start from the end and work our way back in the equation:
# * if the left is divisable by the rightmost element -> divide left and remove the last on the right then recurse with the shorter sequence
# * if not then remove the last element by subtracting the rightmost from the left and recurse
# * end recursion if right is only one element
# Example:
# isValid(190, [10, 19]) -> (10, [10]) OR (171, [10]) -> True OR False
#
# isValid(3267, [81, 40, 27]) -> (121, [81, 40]) OR (3240, [81, 40]) -> (81, [81]) OR (81, [81]) OR (3200, [80]) -> True OR True OR False
def isValid(left, right) -> bool:
    if len(right) == 1:
        return left == right[0]
    return ((left % right[-1] == 0 and isValid(left // right[-1], right[:-1])) or # if divisible then divide and call again
            isValid(left - right[-1], right[:-1])) # else try the substraction

result = sum(l for (l, r) in input if isValid(l, r))
print(result)

#part 2

# same idea but now another operation added for which the recursion rule is:
# * if the left ends with the same digits as the rightmost element -> remove those digits from the left and remove the rightmost element from the sequence
# Example:
# (486, [6, 8, 6]) -> (81, [6, 8]) OR (48, [6, 8]) OR (480, [6, 8]) -> ...
def isValidWithAppend(left, right) -> bool:
    if left < 0 or len(right) == 0: # need to check for negative numbers because the negative sign messes up the str search
        return False
    if len(right) == 1:
        return left == right[0]
    lastRightStr = str(right[-1]) # for readability
    return  ((left % right[-1] == 0 and isValidWithAppend(left // right[-1], right[:-1])) or # as before, if divisible then divide
            (len(lastRightStr) < len(str(left)) and str(left).endswith(lastRightStr) and isValidWithAppend(int(str(left)[:-len(lastRightStr)]), right[:-1])) or # if left ends with right (as str) then remove
            isValidWithAppend(left - right[-1], right[:-1])) # as before, try the subtraction

result = sum(l for (l, r) in input if isValidWithAppend(l, r))
print(result)
