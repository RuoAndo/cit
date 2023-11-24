{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn import datasets, model_selection, svm, metrics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
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
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "     sepal.length  sepal.width  petal.length  petal.width     variety\n",
      "3             4.6          3.1           1.5          0.2      Setosa\n",
      "138           6.0          3.0           4.8          1.8   Virginica\n",
      "72            6.3          2.5           4.9          1.5  Versicolor\n",
      "25            5.0          3.0           1.6          0.2      Setosa\n",
      "122           7.7          2.8           6.7          2.0   Virginica\n",
      "     label\n",
      "3        1\n",
      "138      3\n",
      "72       2\n",
      "25       1\n",
      "122      3\n"
     ]
    }
   ],
   "source": [
    "data_train, data_test, label_train, label_test = model_selection.train_test_split(iris_data, iris_label)\n",
    "print(data_train.head())\n",
    "print(label_train.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "data_train_2 = data_train.drop('variety', axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\ProgramData\\Anaconda3\\lib\\site-packages\\sklearn\\utils\\validation.py:72: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  return f(**kwargs)\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "SVC()"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "clf = svm.SVC()\n",
    "clf.fit(data_train_2, label_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "data_test_2 = data_test.drop('variety', axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'numpy.ndarray'>\n",
      "[2 1 2 2 1 1 2 1 3 3 3 3 3 3 3 2 2 2 3 1 2 2 1 1 1 1 1 2 1 3 1 1 3 1 2 2 3\n",
      " 1]\n"
     ]
    }
   ],
   "source": [
    "pre = clf.predict(data_test_2)\n",
    "\n",
    "print(type(pre))\n",
    "print(pre)"
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
