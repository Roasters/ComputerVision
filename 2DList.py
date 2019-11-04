# image = [[100, 77, 55, 88] for _ in range(3)]
# image[0][0] = 1000
# print(image)
import random

row = 10
col = 10
image = [[random.randint(0, 255) for _ in range(col)] for _ in range(row)]
print(image)