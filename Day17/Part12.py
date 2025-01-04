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

# Part 1
# Trivial, just model each possible commands and run the program
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

# Part 2
# Oh dear oh dear what have I done here... This was the toughest puzzle this year
# And the solution is the ugliest of them all...
#
# So the idea is to run the program backwards, filling the 'gaps' - when unknown numbers creeping into the registers - with all possible variations
# after all it's only the last 3 bits we're usually dealing with (except when we don't)
#
# But it doesn't work properly after a LOT LOT LOT of trial and error.
# Well, it sort of works - the problem is somewhere the sanity check where I should discard the 'impossible' variations
# so it generates a lot of false solutions, but amongst them is the correct one
# 
# Hence the ugly hack is that we collect all the solution candidates, and then run the original program on all of them 
# keeping the one that is actually correct... 
# Turns out it still returns 3... but we only need the smallest number

possible_solutions = set()
def runProgLoopBack(regs: list, prog, ip, lastread):
    lastshift = 0
    while ip >= 0:
        (opc, opd) = prog[ip]
        match opc:
            case 0: #adv
                regs[0] = regs[0] << 3
                for i in range(2**3):
                    possible_solutions.add(regs[0] | i)
            case 1: #bxl
                regs[1] = regs[1] ^ opd

            case 2: #bst
                regs[0] &= ~7
                regs[0] |= (regs[1] & 7)
                # sanity check, is this combination even possible?
                # B = B' ^ C' where C' = A >> B' ... B' is unknown
                if (regs[0] >> lastshift) & 7 != regs[2]:
                    return
            case 4: #bxc
                for i in range(2**3):
                    for j in range(2**3):
                        if i ^ j == regs[1]:
                            r = regs.copy()
                            r[1] = i
                            r[2] = j
                            runProgLoopBack(r, prog, ip-1, lastread)
            case 5: #out
                if lastread < 0:
                    break

                regs[1] = prog[lastread//2][lastread % 2]
                lastread -= 1

            case 7: #cdv
                lastshift = regs[1]
        ip = ip-1 if ip > 0 else len(prog)-1
    regs[0] = regs[0] << 3
    return regs

runProgLoopBack([0,0,0], prog, len(prog)-1, len(prog)*2-1)

possible_solutions = sorted(list(possible_solutions))
solution = 0
for l in possible_solutions:
    s = ','.join(runProg([int(l), 0, 0], prog))
    if s == progstr:
        print(l)
