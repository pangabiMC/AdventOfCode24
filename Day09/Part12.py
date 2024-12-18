import numpy as np

filename = "Day09/input"

with open(filename) as file:
    diskmap = np.array([int(x) for x in file.read()])
diskmap_original = diskmap.copy() # for part 2

# part 1
# We iterate on the whole disk and keeping pointers to the disk map indicating where the defrag is happening
# The 'i' moves forward one step on the disk at a time. For each step we update the checksum.
# fwd_ptr is pointing to the block in the diskmap in which 'i' is currently in
# Every second (even) block is a file that won't move, so if 'i' is within such a block [fwd_ptr % 2 == 0] then ID is simply fwd_ptr / 2
# If the fwd_ptr is odd then we're in an empty space in the original disk, so the ID is coming from the file that is moved here
# This id is pointed by the bck_ptr. 
result = 0
fwd_ptr = 0
bck_ptr = diskmap.size - 1

free_space = sum(diskmap[1::2])
total_length = sum(diskmap)

for i in range(0, total_length - free_space): # no need to go till the whole length of the disk, the end is just free space
    id = 0
    if fwd_ptr % 2 == 0: # this is an block of an original file, not moved
        id = fwd_ptr // 2 # these remain in place, so ID is the index of the file (which is every 2nd index in the map) 
    else:                # this was a free space, let's see what would be moving here
        id = bck_ptr // 2 # the current file being moved from the back
        diskmap[bck_ptr] -= 1 # to keep track of the remaining blocks in the file being moved
        if diskmap[bck_ptr] == 0: # the moved file has no more blocks, jump to the next file to move
            bck_ptr -= 2 # luckily there is no 0 length file in the record, otherwise this would have to skip all zeros
    
    diskmap[fwd_ptr] -= 1 # to keep track of the remaining blocks of the current block (let it be original file or empty)
    if diskmap[fwd_ptr] == 0: # all segments of the current block spent, move to the next block
        fwd_ptr += next((i for i, x in enumerate(diskmap[fwd_ptr:]) if x != 0), None) # move fwd till the next non 0 value (to skip 0 length empty blocks)

    result += i * id

print(result)

# part 2
# the idea roughly: this time move from the back and counting the checksum as we go for each file moved or skipped 
# example
#2333133121414131402
#00...111...2...333.44.5555.6666.777.888899
#0099.111...2...333.44.5555.6666.777.8888..
#0099.1117772...333.44.5555.6666.....8888..
#0099.111777244.333....5555.6666.....8888..
#00992111777.44.333....5555.6666.....8888..
# we start from the last file and jumping from file to file up till the start
# starting with 99 find the first gap that is at least length 2 (first element >= 2 in subarray of diskmap from index 1 to bck_ptr with step 2)
# calculate the checksum for file 99 in this new place. Decrement the length of the gap to avoid putting the next file there. (keep a copy of the map for calculating the real disk positions)
# move to 8888 (bck_ptr moves back by 2), find first gap -> there is none -> calculate checksome at its original place
# and so on until file id 0
diskmap = diskmap_original.copy()
result = 0
for bck_ptr in range(diskmap.size - 1, -1, -2):
    file_id = bck_ptr // 2
    file_length = diskmap[bck_ptr]
    large_enough_empty_blocks = np.argwhere(diskmap[1:bck_ptr:2] >= file_length) # check empty blocks from left to right if they are large enough up till the back_ptr
    if large_enough_empty_blocks.size > 0: # we have a target for this file
        target_block_index = 1 + large_enough_empty_blocks[0][0] * 2
        # sum gives us the start of the empty block, then the diff between the original and the workset map gives us how many blocks have been filled already
        new_start_on_disk = sum(diskmap_original[:target_block_index]) + diskmap_original[target_block_index] - diskmap[target_block_index] 
        diskmap[target_block_index] -= file_length
    else: # not enough space to move this file, add to checksum in its place
        new_start_on_disk = sum(diskmap_original[:bck_ptr])
    
    result += file_id * sum(range(new_start_on_disk, new_start_on_disk + file_length))

print(result)
