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
class Gate:
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

Gates = []
Vars = {}
for l in data:
    if len(l) > 4:
        if l[3] == ':':
            m = re.findall("(\w{3}):\s*(\d+)", l)
            Vars[m[0][0]] = int(m[0][1])
        else:
            m = re.findall("(\w{3})\s*(OR|AND|XOR)\s*(\w{3})\s*->\s*(\w{3})", l)
            Gates.append(Gate(input1=Var(m[0][0], None), input2=Var(m[0][2], None), output=Var(m[0][3], None), operand=m[0][1]))

Gates_copy = Gates.copy() # for Part2

# Part 1
# Simple enough once the data is mapped to the Gate class with its functions
# Just keep on resolving the gates until all is set
while len(Gates) > 0:
    Gates = [o for o in Gates if not o.TrySet(Vars)]

# Read the output from vars beginning with z
zvars = [v for v in Vars if v[0] == 'z']
zvars.sort(reverse=True)
result = 0
for z in zvars:
    result ^= int(Vars[z])
    result = result << 1

print(result // 2)

# Part 2
# Took a hint for this one, I didn't know what a ripple-carry adder was... 
# https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder
# Some observation based on the schematic there (taken from reddit):
#   If the output of a gate is z, then the operation has to be XOR unless it is the last bit.
#   If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR.
#   If you have a XOR gate with inputs x, y, there must be another XOR gate with this gate as an input. 
#   If you have an AND-gate, there must be an OR-gate with this gate as an input. If that gate doesn't exist, the original AND gate is faulty.
#   (These two don't apply for the gates with input x00, y00). 

Gates = Gates_copy

# Checks if the given gate is faulty
def isFaulty(g: Gate) -> bool:
    #   If the output of a gate is z, then the operation has to be XOR unless it is the last bit.
    if g.output.token[0] == 'z' and g.output.token != zvars[0] and g.operand != 'XOR':
        return True
    
    #   If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR.
    if g.output.token[0] != 'z' and g.input1.token[0] not in ['x', 'y'] and g.input2.token[0] not in ['x', 'y'] and g.operand == 'XOR':
        return True
    
    #   If you have a XOR gate with inputs x, y, there must be another XOR gate with this gate as an input.
    if g.operand == 'XOR' and g.input1.token[0] in ['x', 'y'] and g.input2.token[0] in ['x', 'y'] and g.input1.token not in ['x00', 'y00'] and g.input2.token not in ['x00', 'y00']:
        if not any(g_next != g and g_next.operand == 'XOR' and (g_next.input1.token == g.output.token or g_next.input2.token == g.output.token) for g_next in Gates):
            return True
    
    #   If you have an AND-gate, there must be an OR-gate with this gate as an input.
    if g.operand == 'AND' and g.input1.token[0] in ['x', 'y'] and g.input2.token[0] in ['x', 'y'] and g.input1.token not in ['x00', 'y00'] and g.input2.token not in ['x00', 'y00']:
        if not any(g_next != g and g_next.operand == 'OR' and (g_next.input1.token == g.output.token or g_next.input2.token == g.output.token) for g_next in Gates):
            return True
    return False

faulty = [g.output.token for g in Gates if isFaulty(g)]
faulty.sort()
print(','.join(faulty))

