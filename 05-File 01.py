inFp = open("C:/windows/win.ini", "rt") # rt: read text, rb: read binary

inStr = inFp.readlines()
for line in inStr:
    print(line, end='')
inFp.close()

outFp = open("C:/images/new_win.ini", "w")

for line in inStr:
    outFp.writelines(line)

outFp.close()
print("Done")
