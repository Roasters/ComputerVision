# SelectionSort
def selectionSort(myList):
    for i in range(len(myList)):
        for k in range(i+1, len(myList)):
            tmp = myList[i]
            if myList[i] < myList[k]:
                continue
            else:
                myList[i] = myList[k]
                myList[k] = tmp

# BubbleSort
def bubbleSort(myList):
    for i in range(len(myList)-1):
        for k in range(len(myList)-(i+1)):
            tmp = myList[k]
            if myList[k] > myList[k+1]:
                myList[k] = myList[k+1]
                myList[k+1] = tmp

# QuickSort
def quickSort(p, q, myList):
    if p < q:
        r = partition(p, q, myList)
        quickSort(p, r - 1, myList)
        quickSort(r + 1, q, myList)

def partition(p, q, myList):
    i = p - 1
    pivot = myList[q]

    for k in range(p, q):
        if myList[k] <= pivot:
            i += 1
            myList[i], myList[k] = myList[k], myList[i]
    myList[i+1], myList[q] = myList[q], myList[i+1]
    return i + 1

import random
# Sort Hexadecimal Numbers

print("Sort Hexadecimal Numbers\n")
hexList = [hex(random.randint(0, 100)) for _ in range(16)]
hexToInt = list(map(lambda x: int(x, 16), hexList))
print("Before Sorted: ", hexToInt)

mylist = hexToInt[:]
selectionSort(mylist)
print("Sorted by Selection Sort: ", mylist)

mylist = hexToInt[:]
bubbleSort(mylist)
print("Sorted by Bubble Sort: ", mylist)

mylist = hexToInt[:]
quickSort(0, len(mylist)-1, mylist)
print("Sorted by Quick Sort: ", mylist)
print("="*50, "\n")

# Sort Data with Strings and Numbers Mixed Together
print("Sort Data with Strings and Numbers Mixed Together\n")
hexList = [hex(random.randint(0, 100)) for _ in range(16)]
strToInt = [int(''.join([char for char in i if char.isdigit()])) for i in hexList]
print("Before Sorted: ", strToInt)

mylist = strToInt[:]
selectionSort(mylist)
print("Sorted by Selection Sort: ", mylist)

mylist = strToInt[:]
bubbleSort(mylist)
print("Sorted by Bubble Sort: ", mylist)

mylist = strToInt[:]
quickSort(0, len(mylist)-1, mylist)
print("Sorted by Quick Sort: ", mylist)
