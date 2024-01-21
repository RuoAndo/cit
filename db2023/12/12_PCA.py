import sqlite3
import random

import datetime
import random

#import matplotlib as plt
import matplotlib.pyplot as plt

import pandas as pd

dbname = 'cit-db-2023-12.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

comstr = "select * from character;"
#print(comstr)

cur = conn.cursor()
cur.execute(comstr)
conn.commit()

x = []
y = []
z = []

for row in cur:
	#print(row)

	HP = row[3]
	MP = row[4]
	EXP = row[5]

	x.append(HP)
	y.append(MP)
	z.append(EXP)

cur.close()
conn.close()

df = pd.DataFrame({}, index=[])

df = df.assign(HP=x)
df = df.assign(MP=y)
df = df.assign(EXP=z)

#print(df)

from sklearn.decomposition import PCA
pca = PCA()  
pca_x = pca.fit_transform(df)

df_pca = pd.DataFrame(pca_x, columns=['1', '2', '3'])
print(df_pca.head())  

#df_pca.plot()
#print(df_pca['1'])

XX = df_pca['1'].tolist()
YY = df_pca['2'].tolist()

plt.scatter(XX,YY)

plt.title('PCA (character status)')
plt.xlabel('1st component')
plt.ylabel('2nd component')

plt.show()