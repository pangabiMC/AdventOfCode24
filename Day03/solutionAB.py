import re

filename = "Day03/input"
with open(filename) as file:
    data = file.read()

# part 1
regex = "(mul\((\d{1,3}),(\d{1,3})\))"
result = 0
for m in re.findall(regex, data):
    result += int(m[1]) * int(m[2])
print(result)

# part 2
