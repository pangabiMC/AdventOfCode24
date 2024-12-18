import numpy as np
import itertools
filename = "Day15/inputtest"

with open(filename) as file:
    lines = [line.strip() for line in file if len(line.strip()) > 0]

map = np.array([list(l) for l in lines if l[0] == '#'])
movements = list(itertools.chain.from_iterable([list(l) for l in lines if l[0] != '#']))
init_robot_coords = list(zip(*np.where(map == '@')))[0] # find the start pos of the robot
map[init_robot_coords[0]][init_robot_coords[1]] = '.' # we don't need the robot to be on the map anymore, it just complicates movement

# part 1
# we simply simulate all steps the robot takes, taking advantage of the numpy array slicing

# Given a position and a direction the step updates the map and returns the new position of the robot
def step(pos, direction, map) -> tuple:
    shouldMove = False
    match direction:
        case '^':
            cells_ahead = map[pos[0]-1::-1, pos[1]] # this is always going to be the array of remaining cells in the row or column the robot is facing
            newpos = (pos[0]-1, pos[1])
        case '>':
            cells_ahead = map[pos[0], pos[1]+1:]
            newpos = (pos[0], pos[1]+1)
        case 'v':
            cells_ahead = map[pos[0]+1:, pos[1]]
            newpos = (pos[0]+1, pos[1])
        case '<':
            cells_ahead = map[pos[0], pos[1]-1::-1]
            newpos = (pos[0], pos[1]-1)
    
    if cells_ahead[0] == '.':
        shouldMove = True
    else:
        # we either have a wall or a box here
        # if it's a box, we will need to move it to the first .
        first_gap = np.where(cells_ahead == '.')[0]
        first_block = np.where(cells_ahead == '#')[0]

        if len(first_gap) > 0 and first_gap[0] < first_block[0]:
            cells_ahead[0] = '.' # move this box out
            cells_ahead[first_gap[0]] = 'O'
            shouldMove = True
        # else it was a wall or we have a box ahead of us but cannot be moved
    return newpos if shouldMove else pos

robot = init_robot_coords
for m in movements:
    robot = step(robot, m, map)

result = sum(a[0] * 100 + a[1] for a in list(zip(*np.where(map == 'O'))))
print(result)