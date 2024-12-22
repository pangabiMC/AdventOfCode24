import numpy as np
filename = "Day17/inputtest"

with open(filename) as file:
    regA = int(file.readline()[12:])
    regB = int(file.readline()[12:])
    regC = int(file.readline()[12:])
    file.readline()
    prog = list(zip(*[map(int, file.readline()[9:].split(','))]*2))

# part 1
def runProg(regA, regB, regC, prog):
    ip = 0
    for (inst, operand) in prog:
        match


# part 2
