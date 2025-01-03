from dataclasses import dataclass
import re

isTest = False
filename = "Day24/inputtest" if isTest else "Day24/input"

with open(filename) as file:
    data = [line.strip() for line in file]

@dataclass
class Var:
    token: str
    value: int

@dataclass
class Op:
    input1: Var
    input2: Var
    output: Var
    operand: str
    def Calc(self):
        if self.IsSet():
            match self.operand:
                case 'AND':
                    self.output.value = self.input1.value & self.input2.value
                case 'OR':
                    self.output.value = self.input1.value | self.input2.value
                case 'XOR':
                    self.output.value = self.input1.value ^ self.input2.value
    
    def IsSet(self):
        return self.input1.value is not None and self.input2.value is not None
    
    def TrySet(self, vars) -> bool:
        if not self.IsSet():
            if self.input1.token in vars:
                self.input1.value = vars[self.input1.token]
            if self.input2.token in vars:
                self.input2.value = vars[self.input2.token]
            if self.IsSet():
                self.Calc()
                vars[self.output.token] = self.output.value
        return self.IsSet()

Ops = []
Vars = {}
for l in data:
    if len(l) > 4:
        if l[3] == ':':
            m = re.findall("(\w{3}):\s*(\d+)", l)
            Vars[m[0][0]] = int(m[0][1])
        else:
            m = re.findall("(\w{3})\s*(OR|AND|XOR)\s*(\w{3})\s*->\s*(\w{3})", l)
            Ops.append(Op(input1=Var(m[0][0], None), input2=Var(m[0][2], None), output=Var(m[0][3], None), operand=m[0][1]))

Ops2 = Ops.copy() # for Part2

# Part 1
while len(Ops) > 0:
    Ops = [o for o in Ops if not o.TrySet(Vars)]

zvars = [v for v in Vars if v[0] == 'z']
zvars.sort(reverse=True)
result = 0
for z in zvars:
    result ^= int(Vars[z])
    result = result << 1

print(result // 2)

# Part 2
# https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/
#   If the output of a gate is z, then the operation has to be XOR unless it is the last bit.
#   If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR.

#   If you have a XOR gate with inputs x, y, there must be another XOR gate with this gate as an input. 
#       Search through all gates for an XOR-gate with this gate as an input; if it does not exist, your (original) XOR gate is faulty.
#   Similarly, if you have an AND-gate, there must be an OR-gate with this gate as an input. If that gate doesn't exist, the original AND gate is faulty.
#   (These don't apply for the gates with input x00, y00). 

def isFaulty(op: Op) -> bool:
    #   If the output of a gate is z, then the operation has to be XOR unless it is the last bit.
    if op.output.token[0] == 'z' and op.output.token != zvars[0] and op.operand != 'XOR':
        return True
    
    #   If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR.
    if op.output.token[0] != 'z' and op.input1.token[0] not in ['x', 'y'] and op.input2.token[0] not in ['x', 'y'] and op.operand == 'XOR':
        return True
    
    #   If you have a XOR gate with inputs x, y, there must be another XOR gate with this gate as an input.
    if op.operand == 'XOR' and op.input1.token[0] in ['x', 'y'] and op.input2.token[0] in ['x', 'y'] and op.input1.token not in ['x00', 'y00'] and op.input2.token not in ['x00', 'y00']:
        if not any(o != op and o.operand == 'XOR' and (o.input1.token == op.output.token or o.input2.token == op.output.token) for o in Ops2):
            return True
    
    #   If you have an AND-gate, there must be an OR-gate with this gate as an input.
    if op.operand == 'AND' and op.input1.token[0] in ['x', 'y'] and op.input2.token[0] in ['x', 'y'] and op.input1.token not in ['x00', 'y00'] and op.input2.token not in ['x00', 'y00']:
        if not any(o != op and o.operand == 'OR' and (o.input1.token == op.output.token or o.input2.token == op.output.token) for o in Ops2):
            return True
    return False

faulty = [o.output.token for o in Ops2 if isFaulty(o)]
faulty.sort()
print(','.join(faulty))

