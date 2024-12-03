import re

filename = "Day03/input"
with open(filename) as file:
    data = file.read()

# part 1
regex = "(mul\((\d{1,3}),(\d{1,3})\))"
result = sum(int(m[1]) * int(m[2]) for m in re.findall(regex, data))
print(result)

# part 2
#        m[0]    m[1] m[3]  m[4]      m[5]
regex = "(don't)|(do)|(mul\((\d{1,3}),(\d{1,3})\))"
result = 0
do = True
for m in re.findall(regex, data):
    if m[3] and m[4] and do: #it's a mul group
        result += int(m[3]) * int(m[4])
    elif m[1]: # "do"
        do = True
    elif m[0]: # "don't":
        do = False

print(result)