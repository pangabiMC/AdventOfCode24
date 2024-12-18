filename = "Day01/input"
lines = []
with open(filename) as file:
    lines = [line.rstrip() for line in file]

# part 1
l1 = []
l2 = []
for l in lines:
    l1.append(int(l.split()[0]))
    l2.append(int(l.split()[1]))

l1.sort()
l2.sort()

result1 = 0

for i,j in zip(l1, l2):
    result1 += abs(i-j)

print(result1)
 
# part 2
result2 = 0
counts = {i:l2.count(i) for i in l1}
for i in l1:
    result2 += (counts[i] * i)

print(result2)