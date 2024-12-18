import numpy as np 

filename = "Day02/input"
reports = []
with open(filename) as file:
    for line in file:
        reports.append(list(map(int, line.strip().split())))

# part 1
def isSafe(report, skip = -1):
    skipped = report if skip == -1 else report[:skip] + report[skip + 1:]
    diffs = [i - j for i, j in zip(skipped, skipped[1:])]
    return (all(abs(i) <= 3 and abs(i) >= 1 for i in diffs)) and not (min(diffs) < 0 < max(diffs))

print(sum(isSafe(report) for report in reports))

# part 2
c = 0
for report in reports:
    if isSafe(report):
        c += 1
    else:
        for i in range(len(report)):
            if isSafe(report, i):
                c += 1
                break

print(c)

