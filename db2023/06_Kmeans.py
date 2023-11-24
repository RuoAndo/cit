{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn import datasets, model_selection, svm, metrics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "   sepal.length  sepal.width  petal.length  petal.width variety\n",
      "0           5.1          3.5           1.4          0.2  Setosa\n",
      "1           4.9          3.0           1.4          0.2  Setosa\n",
      "2           4.7          3.2           1.3          0.2  Setosa\n",
      "3           4.6          3.1           1.5          0.2  Setosa\n",
      "4           5.0          3.6           1.4          0.2  Setosa\n",
      "   label\n",
      "0      1\n",
      "1      1\n",
      "2      1\n",
      "3      1\n",
      "4      1\n"
     ]
    }
   ],
   "source": [
    "iris_data = pd.read_csv('iris.csv')\n",
    "iris_label = pd.read_csv('iris_label.csv')\n",
    "\n",
    "print(iris_data.head())\n",
    "print(iris_label.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = iris_data[\"sepal.length\"]\n",
    "Y = iris_data[\"sepal.width\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.collections.PathCollection at 0x277fabb5c40>"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.scatter(X,Y)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
