def calc2(*para):  # number of parameters can be varied
    res = 0
    for num in para:
        res += num
    return res

print(calc2(1,2,3,4,5))