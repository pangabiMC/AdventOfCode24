import numpy as np
filename = "Day06/input"

with open(filename) as file:
    matr = np.array([list(line.strip()) for line in file])
length = len(matr[0])

##################################################
# part 1

# Best I can come up with is walking step by step with the guard painting the route as we walk
# The only neat here idea is rotating the matrix beneath the guard rather than tracking which direction it's going

# Paints the row of the guard from the guard to first obstacle with Xs
# Returns the new coordinates for the guards (already rotated by 90 degrees)
def paintMap(guard_coords, matr):
    row = matr[guard_coords[0]][guard_coords[1]:]
    if '#' in row:
        obstacle_index = row.tolist().index('#')
        row[range(0, obstacle_index)] = 'X' # paint
        guard_coords = (length - (obstacle_index + guard_coords[1]), guard_coords[0])
    else:
        row[range(0, len(row))] = 'X'
        guard_coords = None # guard has left the area
    return guard_coords

# Rotate the initial matrix so the guard is facing to the right, not up (just for convenience in indexing)
matr = np.rot90(matr, 3)
init_guard_coords = guard_coords = list(zip(*np.where(matr == '^')))[0] # find the start pos of the guard, also save it for part#2

# Paint, rotate, repeat until the guard has left
guard_left = False
rot_count = 0 # we will need to orient this matr correctly again in part2 so we need to keep track how many times we rotated
while not guard_left:
    guard_coords = paintMap(guard_coords, matr)
    guard_left = guard_coords == None
    matr = np.rot90(matr) # guard turning right
    rot_count += 1

# Answer is the count of Xs we painted
print(np.count_nonzero(matr == 'X'))

##################################################
# part 2

# Bit of a brute force: we take the already painted matrix, and for all Xs try to replace with # and see if it creates a loop

# Gets if the matrix with the original guard starting point will end up in a loop. 
# Same as before, we're walking with the guard, but this time also recording the turning positions
def hasLoop(m):
    orientation = 0
    guard_left = False
    guard_coords = init_guard_coords
    visited_coords = set()
    while not guard_left:
        guard_coords = paintMap(guard_coords, m)
        orientation += 1
        orientation = orientation % 4
        if (guard_coords, orientation) in visited_coords:
            return True
        visited_coords.add((guard_coords, orientation))
        guard_left = guard_coords == None
        m = np.rot90(m) # guard turning right
    return False

matr = np.rot90(matr, 4 - (rot_count % 4)) # rotate the matrix back to the starting position
result = 0
for replace_coords in list(zip(*np.where(matr == 'X'))): # it only makes sense to place an obstacle where the guard originally walked
    working_matr = matr.copy()
    working_matr[replace_coords] = '#'
    if hasLoop(working_matr):
        result += 1

print(result)
