import numpy as np
filename = "Day17/input"
regs = []
with open(filename) as file:
    regs.append(int(file.readline()[12:]))
    regs.append(int(file.readline()[12:]))
    regs.append(int(file.readline()[12:]))
    file.readline()
    prog = list(zip(*[map(int, file.readline()[9:].split(','))]*2))

def get_combo_val(op, regs):
    if 0 <= op <= 3:
        return op
    return regs[op - 4]

# part 1
def runProg(regs, prog):
    output = []
    ip = 0
    while ip // 2 < len(prog):
        (opc, opd) = prog[ip // 2]
        match opc:
            case 0: #adv
                regs[0] = regs[0] >> get_combo_val(opd, regs)
            case 1: #bxl
                regs[1] = regs[1] ^ opd
            case 2: #bst
                regs[1] = get_combo_val(opd, regs) & 7
            case 3: #jnz
                if regs[0] != 0:
                    ip = opd - 2
            case 4: #bxc
                regs[1] = regs[1] ^ regs[2]
            case 5: #out
                output.append(str(get_combo_val(opd, regs) & 7))
            case 6: #bdv
                regs[1] = regs[0] >> get_combo_val(opd, regs)
            case 7: #cdv
                regs[2] = regs[0] >> get_combo_val(opd, regs)
        ip = ip + 2
    return output

print(','.join(runProg(regs, prog)))

# part 2


