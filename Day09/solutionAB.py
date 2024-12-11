import numpy as np

filename = "Day09/input"

with open(filename) as file:
    diskmap = np.array([int(x) for x in file.read()])

map_length = diskmap.size
free_space = sum(diskmap[1::2])
total_length = sum(diskmap)
max_id = diskmap[1::2].size

# part 1
result = 0
fwd_ptr = 0
bck_ptr = map_length - 1
for i in range(0, total_length - free_space):
    id = 0
    if fwd_ptr % 2 == 0:
        # this is an unmoved block
        id = fwd_ptr // 2 
    else:
        # this is a free space
        id = bck_ptr // 2
        diskmap[bck_ptr] -= 1
        if diskmap[bck_ptr] == 0:
            bck_ptr -= 2
    
    diskmap[fwd_ptr] -= 1
    if diskmap[fwd_ptr] == 0:
        fwd_ptr += next((i for i, x in enumerate(diskmap[fwd_ptr:]) if x != 0), None)
        
    result += i * id

# with open('./output_file.dat', "w+") as mat_PM:
#     np.savetxt(mat_PM, ids, fmt='%d', delimiter=" ")
print(result)
#print(' '.join(map(str, ids)))

# part 2
with open(filename) as file:
    diskmap = np.array([int(x) for x in file.read()])

result = 0
fwd_ptr = 0
bck_ptr = map_length - 1
for i in range(0, total_length - free_space):
    id = 0
    if fwd_ptr % 2 == 0:
        # this is an unmoved block
        id = fwd_ptr // 2 
    else:
        # this is a free space
        id = bck_ptr // 2
        diskmap[bck_ptr] -= 1
        if diskmap[bck_ptr] == 0:
            bck_ptr -= 2
    
    diskmap[fwd_ptr] -= 1
    if diskmap[fwd_ptr] == 0:
        fwd_ptr += next((i for i, x in enumerate(diskmap[fwd_ptr:]) if x != 0), None)
        
    result += i * id

# with open('./output_file.dat', "w+") as mat_PM:
#     np.savetxt(mat_PM, ids, fmt='%d', delimiter=" ")
print(result)
#print(' '.join(map(str, ids)))
