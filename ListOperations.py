import random
myList = [random.randint(1,5) for _ in range(20)]
print(myList)
num = 5

i = 0
while True:
    try:
        idx = myList.index(num, i)
        print(idx)
        i = idx + 1
    except:
        break