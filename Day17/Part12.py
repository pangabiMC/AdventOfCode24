import math
from contextlib import redirect_stdout
filename = "Day17/input"
regs = []
with open(filename) as file:
    regs.append(int(file.readline()[12:]))
    regs.append(int(file.readline()[12:]))
    regs.append(int(file.readline()[12:]))
    file.readline()
    progstr = file.readline()[9:]
    prog = list(zip(*[map(int, progstr.split(','))]*2))
    
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

def runProgLoopBack(regs: list, prog, ip, lastread, lastshift):
    while ip >= 0 and lastread >= 0:
        (opc, opd) = prog[ip]
        match opc:
            case 0: #adv
                l = get_combo_val(opd, regs)
                regs[0] = regs[0] << l

                # if regs[0] != regs[1] --> return None
                # if l > 3
                #   for i in range(2**(l-3)):
                #       r = regs.copy()
                #       r[0] = r[0] ^ i
                #       runProgLoopBack(r, prog, ip - 1, lastread)
            case 1: #bxl
                regs[1] = regs[1] ^ opd

            case 2: #bst
                regs[0] &= ~7
                regs[0] |= (regs[1] & 7)
                if (regs[0] >> lastshift) & ~7 != regs[2]:
                    return None

            case 4: #bxc
                for i in range(2**3):
                    for j in range(2**3):
                        if i ^ j == regs[1]:
                            print(f'B == {regs[1]} = {i} ^ {j}')
                for i in range(2**3):
                    for j in range(2**3):
                        if i ^ j == regs[1]:
                            r = regs.copy()
                            r[1] = i
                            r[2] = j
                            runProgLoopBack(regs, prog, ip-1, lastread, lastshift)
            case 5: #out
                regs[opd - 4] &= ~7
                regs[opd - 4] |= prog[lastread//2][lastread % 2]
                lastread -= 1

            case 7: #cdv
                regs[2] = regs[0] << regs[1]
                lastshift = regs[1]


        ip = ip-1 if ip > 0 else len(prog)-1
    regs[0] = regs[0] << 3
    print(regs)
    return regs

runProgLoopBack([0,0,0], prog, len(prog)-1, len(prog)*2-1, 0)

print(len(prog))

# regs = [0, 0, 0]
# with open('out2.txt', 'w') as f:
#     with redirect_stdout(f):
#         for i in range(0, 2561):
#             a = i # 2 ** (3 + 2*i*3)
#             o = ','.join(runProg([a, 0, 0], prog))
#             print(f'{i} - {a} {o}')
# a = 2 ** (3 + 2*7*3)-1
# b = 2 ** (3 + 2*8*3)-1
# print(b-a)
# print(','.join(runProg([a, 0, 0], prog)))
# print(','.join(runProg([a+1, 0, 0], prog)))
# print(','.join(runProg([a+2, 0, 0], prog)))


#counter = 2 ** (3 + 2* (len(prog) - 1) * 3)
# while not ','.join(runProg([counter, 0, 0], prog)) == progstr:
#     counter += 1
#     if counter % 10000 == 0:
#         print(counter, end="\r")
# print()
# print(counter)