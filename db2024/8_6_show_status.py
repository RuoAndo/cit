import sqlite3
import random

import datetime
import random

#import matplotlib as plt
import matplotlib.pyplot as plt

dbname = 'cit-db-2024-08.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

comstr = "select * from character;"
print(comstr)

cur = conn.cursor()
cur.execute(comstr)
conn.commit()

x = []
y = []
z = []

for row in cur:
	print(row)

	HP = row[3]
	MP = row[4]
	EXP = row[5]

	x.append(HP)
	y.append(MP)
	z.append(EXP)

cur.close()
conn.close()

##

fig = plt.figure(figsize = (8, 8))

ax = fig.add_subplot(111, projection='3d')

ax.set_title("character status", size = 20)

ax.set_xlabel("HP", size = 14, color = "r")
ax.set_ylabel("MP", size = 14, color = "r")
ax.set_zlabel("EXP", size = 14, color = "r")

#ax.set_xticks([-5.0, -2.5, 0.0, 2.5, 5.0])
#ax.set_yticks([-5.0, -2.5, 0.0, 2.5, 5.0])

ax.scatter(x, y, z, s = 40, c = "blue")
plt.show()