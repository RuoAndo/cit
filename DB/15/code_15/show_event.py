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

cur.execute("select * from events where person_ID = 1 and character_ID = 1;")
for row in cur.fetchall():
	print(row)
	HPList.append(row[6])

print(HPList)

import matplotlib.pyplot as plt

plt.plot(HPList)
plt.show()

cur.close()
conn.close()
