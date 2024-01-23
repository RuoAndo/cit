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

# To check recent matplotlib compatibility
import matplotlib
from distutils.version import LooseVersion
import numpy as np

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):

    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], 
                    y=X[y == cl, 1],
                    alpha=0.8, 
                    color=colors[idx],
                    marker=markers[idx], 
                    label=cl, 
                    edgecolor='black')

    # highlight test examples
    if test_idx:
        # plot all examples
        X_test, y_test = X[test_idx, :], y[test_idx]

        if LooseVersion(matplotlib.__version__) < LooseVersion('0.3.4'):
            plt.scatter(X_test[:, 0],
                        X_test[:, 1],
                        c='',
                        edgecolor='black',
                        alpha=1.0,
                        linewidth=1,
                        marker='o',
                        s=100, 
                        label='test set')
        else:
            plt.scatter(X_test[:, 0],
                        X_test[:, 1],
                        c='none',
                        edgecolor='black',
                        alpha=1.0,
                        linewidth=1,
                        marker='o',
                        s=100, 
                        label='test set')  

X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5, 
                           p=2, 
                           metric='minkowski')
knn.fit(X_train_std, y_train)

plot_decision_regions(X_combined_std, y_combined, 
                      classifier=knn, test_idx=range(105, 150))

plt.xlabel('petal length [standardized]')
plt.ylabel('petal width [standardized]')
plt.legend(loc='upper left')
plt.tight_layout()
#plt.savefig('images/03_24.png', dpi=300)
plt.show()

