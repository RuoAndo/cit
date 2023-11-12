#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

import time
import datetime

dbname = 'TEST.db'
# データベースに接続
conn = sqlite3.connect(dbname)

# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

sql = """DROP TABLE IF EXISTS XY"""
conn.execute(sql)

cur.execute(
    'CREATE TABLE XY(id INTEGER PRIMARY KEY AUTOINCREMENT, x INTEGER, y INTERGER)')

conn.commit()

start = time.time() 

for i in range(10000):

	x = random.randint(1, 100)
	y = random.randint(1, 100)

	#id = random.randint(101,1000)
	#print(id)

	#commstr = "'INSERT INTO XY values(1,3,2)'"
	commstr = "INSERT INTO XY values(" + str(i) + "," + str(x) + "," + str(y) + ");"
	#print(commstr)
	cur.execute(commstr)
	conn.commit()
	
	if i % 100 == 0:
		dt_now = datetime.datetime.now()
		print("[" + str(dt_now) + "] " + "INSERT " + str(i) + " times done.")
	
#conn.commit()

end = time.time() 
time_diff = end - start  
print(time_diff)  

# 5.データベースの接続を切断
cur.close()
conn.close()