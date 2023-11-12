import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

input_csv = pd.read_csv('./test.log')
first_column_data = input_csv[input_csv.keys()[0]]
second_column_data = input_csv[input_csv.keys()[1]]

plt.xlabel(input_csv.keys()[0])
plt.ylabel(input_csv.keys()[1])
#print(input_csv.keys()[0])

X = input_csv.iloc[:, 0]
X = X.astype(str)
#print(X)

ticks = 5
plt.xticks(np.arange(0, len(X), ticks), X[::ticks], rotation=60)
plt.plot(first_column_data, second_column_data, linestyle='solid', marker='o')
plt.show()
