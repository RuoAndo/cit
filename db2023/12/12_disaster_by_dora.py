import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

import sqlite3
import random

# Generate sample data
n_samples = 1000
n_components = 2

X, y = make_blobs(n_samples=n_samples,
                       centers=n_components,
                       cluster_std=1,
                       random_state=100)

X1 = X[:, 0]*10 + 50
X2 = X[:, 1]*10 + 100

#fig, ax = plt.subplots(dpi=140,figsize=(4,4))
#ax.axis("equal")
#plt.scatter(X1, X2, c=y, marker='o',alpha=0.5,s=55,linewidths=.1,edgecolor="k",cmap="turbo")
#ax.set(xlabel="x",ylabel="y")
#plt.show()

#for i in range(1000):
#	print(int(X1[i]))

dbname = 'cit-db-2023-12.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

for i in range(1000):
	HP_tmp = int(X1[i])
	MP_tmp = int(X2[i])

	print("! " + str(HP_tmp) + " : " + str(MP_tmp))

	comstr = "update character set HP = " + str(HP_tmp) + " where character_id = " + str(i) + ";"
	cur = conn.cursor()
	cur.execute(comstr)
	conn.commit()

	comstr = "update character set MP = " + str(MP_tmp) + " where character_id = " + str(i) + ";"
	cur = conn.cursor()
	cur.execute(comstr)
	conn.commit()

cur.close()
conn.close()