from dataclasses import dataclass
import re

isTest = False
filename = "Day24/inputtest" if isTest else "Day24/input"

with open(filename) as file:
    data = [line.strip() for line in file]

@dataclass
class Op:
    input1: str
    input2: str
    output: str
    operand: str
    def Calc(self):
        if self.IsSet():
            match self.operand:
                case 'AND':
                    self.output = str(int(self.input1) & int(self.input2))
                case 'OR':
                    self.output = str(int(self.input1) | int(self.input2))
                case 'XOR':
                    self.output = str(int(self.input1) ^ int(self.input2))
    def IsSet(self):
        return self.input1 in ['0', '1'] and self.input2 in ['0', '1']
    def TrySet(self, vars) -> bool:
        if not self.IsSet():
            if self.input1 in vars:
                self.input1 = vars[self.input1]
            if self.input2 in vars:
                self.input2 = vars[self.input2]
            if self.IsSet():
                t = self.output
                self.Calc()
                vars[t] = self.output
        return self.IsSet()

Ops = []
Vars = {}

for l in data:
    if len(l) > 4:
        if l[3] == ':':
            m = re.findall("(\w{3}):\s*(\d+)", l)
            Vars[m[0][0]] = m[0][1]
        else:
            m = re.findall("(\w{3})\s*(OR|AND|XOR)\s*(\w{3})\s*->\s*(\w{3})", l)
            Ops.append(Op(input1=m[0][0], input2=m[0][2], output=m[0][3], operand=m[0][1]))

while len(Ops) > 0:
    Ops = [o for o in Ops if not o.TrySet(Vars)]

zvars = [v for v in Vars if v[0] == 'z']
zvars.sort(reverse=True)
result = 0
for z in zvars:
    result ^= int(Vars[z])
    result = result << 1

print(result // 2)

