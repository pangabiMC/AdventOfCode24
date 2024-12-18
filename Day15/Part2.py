import numpy as np
import itertools

filename = "Day15/input"

with open(filename) as file:
    lines = [line.strip() for line in file if len(line.strip()) > 0]

# Duplicates all characters in a row of the map given the rules of the puzzle
def duplicate_line(line) -> list:
    line = ''.join([ch*2 for ch in line])
    line = line.replace("@@", "@.").replace("OO", "[]")
    return list(line)

# Read the input
map = np.array([duplicate_line(l) for l in lines if l[0] == '#'])
movements = list(itertools.chain.from_iterable([list(l) for l in lines if l[0] != '#']))
init_robot_coords = list(zip(*np.where(map == '@')))[0] # find the start pos of the robot
map[init_robot_coords[0]][init_robot_coords[1]] = '.' # we don't need the robot to be on the map anymore, it just complicates movement

# Given a position that points to a crate, a direction and the map,
# it returns the coordinates of the new cells the crate would have to be occupying if pushed towards the given direction
# This will return two points if we're pushing up or down (as the crates are two wide) but only one if going left or right (as it's only taking up 1 new cell)
def get_next_shift_pos(pos, direction, map):
    box = map[pos]
    offset = 1 if box == '[' else -1
    match direction:
        case '^':
            newpos = [(pos[0]-1, pos[1]), (pos[0]-1, pos[1] + offset)]
        case '>':
            newpos = [(pos[0], pos[1]+2)]
        case 'v':
            newpos = [(pos[0]+1, pos[1]), (pos[0]+1, pos[1] + offset)]
        case '<':
            newpos = [(pos[0], pos[1]-2)]
    return newpos

# Given a position that points to a crate, a direction and the map,
# it recursively checks if the crate on that position can be pushed the given direction
# If there are multiple crates stacked after each other, this will walk all of them
def can_shift_box(pos, direction, map) -> bool:
    can_shift = False
    next_pos = get_next_shift_pos(pos, direction, map)
    if map[pos] == '.' or all(map[n] == '.' for n in next_pos):
        can_shift = True
    elif any(map[n] == '#' for n in next_pos):
        can_shift = False
    else:
        can_shift = all([can_shift_box(n, direction, map) for n in next_pos])

    return can_shift

# Given a position that points to a crate that can be moved(!!!), a direction and the map,
# this updates the map with the crate(s) pushed
def shift_boxes(pos, direction, map):
    box = map[pos]
    offset = 1 if box == '[' else -1
    next_pos = get_next_shift_pos(pos, direction, map)
    match direction:
        case '^': 
            for n in next_pos:
                if map[n] == '[' or map[n] == ']':
                    shift_boxes(n, direction, map)
            
            map[pos] = '.'
            map[(pos[0], pos[1]+offset)] = '.'
            map[(pos[0]-1, pos[1])] = box
            map[(pos[0]-1, pos[1] + offset)] = ']' if offset == 1 else '['
        
        case '>':
            if map[next_pos[0]] == '[':
                shift_boxes(next_pos[0], direction, map)

            map[next_pos[0]] = ']'
            map[(pos[0], pos[1]+1)] = '['
            map[pos] = '.'
        
        case 'v':
            for n in next_pos:
                if map[n] == '[' or map[n] == ']':
                    shift_boxes(n, direction, map)
            
            map[pos] = '.'
            map[(pos[0], pos[1]+offset)] = '.'
            map[(pos[0]+1, pos[1])] = box
            map[(pos[0]+1, pos[1] + offset)] = ']' if offset == 1 else '['
        
        case '<':
            if map[next_pos[0]] == ']':
                shift_boxes(next_pos[0], direction, map)

            map[next_pos[0]] = '['
            map[(pos[0], pos[1]-1)] = ']'
            map[pos] = '.'

# Given a position and a direction the step updates the map and returns the new position of the robot
def step(pos, direction, map) -> tuple:
    shouldMove = False
    match direction:
        case '^':
            newpos = (pos[0]-1, pos[1])
        case '>':
            newpos = (pos[0], pos[1]+1)
        case 'v':
            newpos = (pos[0]+1, pos[1])
        case '<':
            newpos = (pos[0], pos[1]-1)
    
    if map[newpos] == '.':
        shouldMove = True
    elif map[newpos] == '#':
        shouldMove = False
    elif can_shift_box(newpos, direction, map):
        shift_boxes(newpos, direction, map)
        shouldMove = True
    return newpos if shouldMove else pos


robot = init_robot_coords
for m in movements:
    robot = step(robot, m, map)

result = sum(a[0] * 100 + a[1] for a in list(zip(*np.where(map == '['))))
print(result)