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

plt.scatter(HPList,EXPList)

plt.title('Character status')
plt.xlabel('HP')
plt.ylabel('EXP')
plt.show()

cur.close()
conn.close()
