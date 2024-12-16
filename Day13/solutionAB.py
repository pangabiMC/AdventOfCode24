import re
filename = "Day13/input"

regex_btnA = "Button\s*A:\s*X([+|-]\d+),\s*Y([+|-]\d+)"
regex_btnB = "Button\s*B:\s*X([+|-]\d+),\s*Y([+|-]\d+)"
regex_prize = "Prize:\s*X=([+|-]?\d+),\s*Y=([+|-]?\d+)"

with open(filename) as file:
    data = file.read()

# processing the input data, we're making linear system with the coefficients in a list:
# example:
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
# this means that:
# 94*x + 22*y = 8400 
# 34*x + 67*y = 5400
# where lowercase x, y will mean the number of times button A and B is pressed.
# We can think of these as lines in a 2D space (Ax+By-C=0) and where the two lines have an intersection, that's our solution for the given machine
# Note that there is only one or 0 solution per machine (the script sayint the "minimum" is sought is misleading)
# We also need to check if the intersection points are whole numbers (you can't push a button a fraction)

# Gets the list of coefficients, ie [((94, 22, 8400), (34, 67, 5400)), ...
def get_machines(data, isPart2 = False):
    btnAVals = re.findall(regex_btnA, data)
    btnBVals = re.findall(regex_btnB, data)
    prizeVals = re.findall(regex_prize, data)
    displace = 10000000000000 if isPart2 else 0 # this is the only difference in part 2
    rules_x = [*zip((int(a[0]) for a in btnAVals), (int(b[0]) for b in btnBVals), (int(p[0]) + displace for p in  prizeVals))]
    rules_y = [*zip((int(a[1]) for a in btnAVals), (int(b[1]) for b in btnBVals), (int(p[1]) + displace for p in  prizeVals))]
    return [*zip(rules_x, rules_y)]

# Gets the coordinates where two lines intersect (aka the solution to the linear system)
# See Cramer's rule https://en.wikipedia.org/wiki/Cramer%27s_rule
# and https://stackoverflow.com/a/20679579
def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def solve(isPart2 = False):
    result = 0
    for m in get_machines(data, isPart2):
        i = intersection(m[0], m[1])
        if i and i[0].is_integer() and i[1].is_integer():
            result += int(i[0]) * 3 + int(i[1])
    return result

print(solve()) # part 1
print(solve(True)) # part 2
