#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time
import datetime

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

i = 0

while i < 500:

	# 2.sqliteを操作するカーソルオブジェクトを作成
	cur = conn.cursor()
	cur.execute('select * from events')

#comstr2 = "create table events (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), event_type VARCHAR(20), event_time VARCHAR(20), event_counter INTEGER);"

	print("EVENT:")
	for row in cur:
		#print(row)	

		constr = "{"
		constr = constr + "person_id : " + str(row[0])
		constr = constr + ", "	
		constr = constr + "charater_id : " + str(row[1])
		constr = constr + ", "	
		constr = constr + "charater_name : " + str(row[2])
		constr = constr + ", "	
		constr = constr + "event_type : " + str(row[3])
		constr = constr + ", "	
		constr = constr + "event_time : " + str(row[4])
		constr = constr + ", "	
		constr = constr + "event_counter : " + str(row[5])
		constr = constr + ", "
		constr = constr + "HP : " + str(row[6])
	
		constr = constr + "}"
	
		print(constr)

	print("--- ---")

	time.sleep(5)
    
# 5.データベースの接続を切断
cur.close()
conn.close()

