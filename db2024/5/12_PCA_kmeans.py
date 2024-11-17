import sqlite3
import random

import datetime
import random

#import matplotlib as plt
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

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

df_km = pd.DataFrame({}, index=[])
df_km = df.assign(X=XX)
df_km = df.assign(Y=YY)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=1)
kmeans.fit(df_km)

distances = kmeans.transform(df_km)
#print(distances.flatten())

sorted_idx = np.argsort(distances.ravel())[::-1][:5] 
print(sorted_idx)

print("anomaly " + str(distances.flatten()[sorted_idx[0]]))
print(XX[sorted_idx[0]])
print(YY[sorted_idx[0]])

f, ax = plt.subplots(figsize=(7, 5))
ax.set_title("Single Cluster")

XXX = XX[sorted_idx[0]]
YYY = YY[sorted_idx[0]]

ax.scatter(XX, YY)
ax.plot(XXX, YYY,label='Extreme Value',marker='o', markersize=20, color='r')
#ax.plot(10,10)

#ax.scatter(XX,YY)
#ax.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:, 1],label='Centroid', color='r')
#ax.scatter(XXYY[sorted_idx][:, 0], XXYY[sorted_idx][:, 1],label='Extreme Value', edgecolors='g',facecolors='none', s=100)
#ax.scatter(a_2d_jagged[:, 0], a_2d_jagged[:, 1], label='Points')
#ax.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:, 1],label='Centroid', color='r')
#ax.scatter(XX[sorted_idx][:, 0], YY[sorted_idx][:, 1],label='Extreme Value', edgecolors='g',facecolors='none', s=100)
#ax.legend(loc='best')
plt.show()

#data = {}
#df = pd.DataFrame(data)
#df['HP'] = XX
#df['MP'] = YY

#l_2d_jagged = [XX,YY]
#a_2d_jagged = np.array(l_2d_jagged, dtype=object)
#print(l_2d_jagged)

#print(df)

#from sklearn.cluster import KMeans
#kmeans = KMeans(n_clusters=1)
#kmeans.fit(XX,YY)

#distances = kmeans.transform(l_2d_jagged)
#print(distances)

#sorted_idx = np.argsort(distances.ravel())[::-1][:5] 
#print(sorted_idx)

#f, ax = plt.subplots(figsize=(7, 5))
#ax.set_title("Single Cluster")
#ax.scatter(XX,YY)
#ax.scatter(a_2d_jagged[:, 0], a_2d_jagged[:, 1], label='Points')
#ax.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:, 1],label='Centroid', color='r')
#ax.scatter(XX[sorted_idx][:, 0], YY[sorted_idx][:, 1],label='Extreme Value', edgecolors='g',facecolors='none', s=100)
#ax.legend(loc='best')
#plt.show()

#plt.scatter(XX,YY)

#plt.title('PCA (character status)')
#plt.xlabel('1st component')
#plt.ylabel('2nd component')
#plt.show()