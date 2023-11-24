import random
import matplotlib.pyplot as plt 

cycle = 1000

val_list = [1,2,3,4,5]
result_list = [random.choices(val_list)[0] for _ in range(cycle)]

print(result_list)

plt.hist(result_list)
plt.show()