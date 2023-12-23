import numpy as np
import matplotlib.pyplot as plt

data_set = np.loadtxt(
    fname="9_1.csv",
    dtype="int",
    delimiter=",",
)

for data in data_set:
    plt.scatter(data[0], data[1])

plt.title("status")
plt.xlabel("HP")
plt.ylabel("MP")
plt.grid()

plt.show()
