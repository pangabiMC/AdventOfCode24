import numpy as np
filename = "Day04/input"

with open(filename) as file:
    matr = np.array([list(line.strip()) for line in file])
length = len(matr[0])

# part 1 - rotating the matrix by 90 four times and checking the diagonals on each rotation
result = 0
for i in range(0, 4):
    r = np.rot90(matr, i)
    result += sum((''.join(l)).count("XMAS") for l in r)
    result += sum((''.join(np.diagonal(r, j))).count("XMAS") for j in range(-length, length))
print(result)

# part 2 - takes all possible 3x3 submatrices and checks diagonals for strings of SAM or MAS
def isXMas(m):
    return ((''.join(np.diagonal(m)) in ("MAS", "SAM")) and 
            (''.join(np.diagonal(np.rot90(m))) in ("MAS", "SAM")))

subMatrices = [matr[i : i + 3, j : j + 3] for i in range(0, length-2) for j in range(0, length-2)]
print(sum(isXMas(subM) for subM in subMatrices))
