import operator
from collections import defaultdict

ttL = [("Thomas", 5), ("Henry", 8), ("Edward", 9), ("Thomas", 12), ("Edward", 1), ("Gordon", 17)]

totalRank, currentRank = 1, 1

tD = defaultdict(int)
for name, weight in ttL:
    tD[name] += weight

print("Train Weight List => ", ttL)
print('-'*30)
tL = sorted(tD.items(), key=operator.itemgetter(1), reverse=True)

print("Train \tTotal Weight \tRank")
print('-'*30)

print(tL[0][0], '\t\t', tL[0][1], '\t\t', currentRank)
for i in range(1, len(tL)):
    totalRank += 1
    if tL[i][1] == tL[i-1][1]:
        pass
    else:
        currentRank = totalRank
    print(tL[i][0], '\t\t', tL[i][1], '\t\t', currentRank)
