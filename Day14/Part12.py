import re
from contextlib import redirect_stdout
test = False
filename = "Day14/inputtest" if test else "Day14/input"

input_pattern = "p=([+|-]?\d+),([+|-]?\d+)\s*v=([+|-]?\d+),([+|-]?\d+)" # input is like "p=0,4 v=3,-3"
width = 11 if test else 101
height = 7 if test else 103

# part 1
# This is just toooo easy. Each robot's final position is just the initial pos + velocity * iterations and because of the "transportation" rule
# we just simply get the modulo with the map's dimensions
iterations = 100

with open(filename) as file:
    robot_init = list(((int(match[0]), int(match[1])), (int(match[2]), int(match[3]))) for match in re.findall(input_pattern, file.read())) # [(('0', '4'), ('3', '-3')), ...

def step(robots : list, iteration: int) -> list:
    return list(((p[0] + iteration * v[0]) % width, (p[1] + iteration * v[1]) % height) for (p, v) in robots)

robot_final = step(robot_init, iterations)

# then sort it into quadrants... too easy... something is brewing here...
result = (sum(r[0] < width // 2 and r[1] < height // 2 for r in robot_final) *
          sum(r[0] > width // 2 and r[1] < height // 2 for r in robot_final) *
          sum(r[0] < width // 2 and r[1] > height // 2 for r in robot_final) *
          sum(r[0] > width // 2 and r[1] > height // 2 for r in robot_final))
print(result)

# part 2
# ooooh my ...
# Ok this is silly but without the puzzle defining what a christmas tree is, we haven't got many options
# One idea would be to check if there are large enough number of robots standing in a straight line
# Or diagonal lines...
# But how many is enough?
# Sooo instead let's print each iterations in a file and keep it watching until we see something interesting...
# ...
# oh yeah... after a while we notice that sometimes column 40 and 70 get crowded... suspiciously round numbers
# so let's just focus on those iterations where these lines are crowded (what crowded means?... well trial and error)
# we could then say that perhaps these two lines will completely filled on the solution (but no)
# so let's instead just print all those iterations that satisfy this crowded condition up till a reasonably large number
# then using notepad scroll until you spot the tree... 
# elegant... hell no. Do I want to move on... hell yeah.
def printRobots(robots):
    for i in range(0, width):
        for j in range(0, height):
            if (j, i) in robots:
                print('1', end='')
            else:
                print('.', end='')
        print()

threshold = 30
with open('out2.txt', 'w') as f:
    with redirect_stdout(f):
        for i in range(0, 10000):
            robots = step(robot_init, i)
            l1 = sum(1 for r in robots if r[0] == 40)
            l2 = sum(1 for r in robots if r[0] == 70)
            if l1 > threshold and l2 > threshold:
                print(f"--------------------------------- {i} ---------------------------------")
                printRobots(robots)
