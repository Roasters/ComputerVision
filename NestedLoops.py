for i in range(2, 10):
    for k in range(1, 10):
        print(i, "*", k, "=", i * k)

import random
data = [random.randint(0, 99) for _ in range(10)]
new_data = []
for i in range(len(data)):
    new_data.append(data[i] + 10)

print(data)
print(new_data)
