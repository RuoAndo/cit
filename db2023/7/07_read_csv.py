import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

a1 = pd.read_csv("1.csv",header=None, parse_dates=True, names=("_time", "c1","c2","c3","c4","c5","c6","c7","c8","c9","c10"))
#a1 = pd.read_csv("1.csv",header=False, parse_dates=True)
#a1.plot()

a2=a1[2:]
#print(a2["_time"]+","+a2["c1"])
X=a2['c1'].astype(float).astype(int)


fig, ax = plt.subplots(facecolor="w")
ax.plot(a2["_time"], X)

#ax.set_xticks([])
#ax.set_yticks([])

L=len(a2.index)
print(L)

plt.xticks(np.arange(0, L+1, 10),rotation=90)
plt.show()
