#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

for i in range(100000):

	x = random.randint(1, 100)
	y = random.randint(1, 100)

	id = random.randint(101,1000)
	print(id)

	#commstr = "'INSERT INTO XY values(1,3,2)'"
	commstr = "INSERT INTO XY values(" + str(id) + "," + str(x) + "," + str(y) + ");"
	#print(commstr)
	cur.execute(commstr)
	

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()