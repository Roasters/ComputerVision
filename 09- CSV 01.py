import csv

# Average income
# income = 0
# with open("C:/images/csv/Emp.csv") as rfp:
#     lines = rfp.readlines()
#     for line in lines[1:]:
#         line = line.strip()
#         line = line.split(',')
#         income += int(line[-1])
#
# print(income / (len(lines)-1))

with open("C:/images/csv/Emp.csv") as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    sum = 0
    count = 0
    for cList in reader:
        sum += int(cList[3])
        count += 1
    avg = sum // count
    print(avg)


