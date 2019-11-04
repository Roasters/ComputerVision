import csv
import random
from tkinter.filedialog import *

filename = askopenfilename(parent=None, filetypes=(("CSV File", "*.csv"), ("All File", "*.*")))

csvList = []

with open(filename) as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    for cList in reader:
        csvList.append(cList)

## Increase price by 10%
# 1. Find the index of Cost column
headerList = [data.upper().strip() for data in headerList]
pos = headerList.index("COST")

# 2. Change the cost value
for i in range(len(csvList)):
    price = float(csvList[i][pos][1:].strip())
    csvList[i][pos] = "${:.2f}".format(price * 1.1)

# 3. Save the result
saveFp = asksaveasfile(parent=None, mode='wt', defaultextension="*.csv", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")))
with open(saveFp.name, "w", newline='') as wFp:
    writer = csv.writer(wFp)
    writer.writerow(headerList)
    for row in csvList:
        writer.writerow(row)

