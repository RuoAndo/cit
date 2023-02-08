#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

HPList = []
EXPList = []

cur.execute("select * from character;")
for row in cur.fetchall():
	print(row)
	HPList.append(row[3])
	EXPList.append(row[5])

print(HPList)

import matplotlib.pyplot as plt
#plt.scatter(HPList,EXPList)
#plt.title('Character status')
#plt.xlabel('HP')
#plt.ylabel('EXP')
#plt.show()

from sklearn.datasets import make_blobs
X, labels = make_blobs(100, centers=1)
import numpy as np

print(X)


#b = [[]]
a = []
#b = np.ones((100,2),int)
#print(b)

counter = 0

c = np.zeros((1,2))
#print(c)
for i in HPList:
	a = []
	a.append(i)
	a.append(EXPList[counter])
	#c.append(np.array(a))
	#print(np.array(a))
	#c= np.append(c, np.array(a))
	c = np.vstack((c, np.array(a)))
	#b.append(np.array(a))
	
	counter = counter + 1
	
c = np.delete(c,0,0)
print(c)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=1)
kmeans.fit(c)

#import matplotlib.pyplot as plt

#f, ax = plt.subplots(figsize=(8, 5))
#ax.set_title("Blob")
#ax.scatter(c[:, 0], c[:, 1], label='Points')
#ax.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:, 1], label='Centroid',color='r')
#ax.legend()
#plt.show()

distances = kmeans.transform(c)
sorted_idx = np.argsort(distances.ravel())[::-1][:5] 

f, ax = plt.subplots(figsize=(7, 5))
ax.set_title("Single Cluster")
ax.scatter(c[:, 0], c[:, 1], label='Points')
ax.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:, 1],label='Centroid', color='r')
ax.scatter(c[sorted_idx][:, 0], c[sorted_idx][:, 1],label='Extreme Value', edgecolors='g',facecolors='none', s=100)
ax.legend(loc='best')

plt.show()

cur.close()
conn.close()