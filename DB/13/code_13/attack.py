#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time
import datetime

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

#cur.execute('select * from character;')
#for row in cur:
#	print(row)

cur.execute('select * from character;')
for row in cur:
	
	#print(row)
	cur = conn.cursor()
	strhp = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])

	playerID = row[0]
	charaID = row[1]
	charaName = row[2]
	
	damage = random.randint(10, 20)	
	currentHP = row[3]
	nextHP = currentHP - damage
	
	print("test damage:" + str(damage))
	
	comstr = "update character set HP=" + str(nextHP) + " where character_id = " + str(charaID) + " and person_id=" + str(playerID) + ";"
	print(comstr)
	
	now = datetime.datetime.now()
	
	print("Event: " + str(now))
	print(" SQL: " + comstr)
	cur.execute(comstr)
	conn.commit()
	
	comstr="select COUNT(*) from events;"
	cur.execute(comstr)

	result = cur.fetchall()
	#print (result)
	record_max = result[0][0]
	#print (record_max)

	current_count = record_max + 1;

	comstr = "insert into events (person_id, character_id, character_name, event_type, event_time, event_counter, HP) values(" + str(playerID) + "," + str(charaID) + "," + "'" + str(charaName) + "'" + "," + "'attack'," + "'" + str(now) + "'" + "," + str(current_count) + "," + str(currentHP) + ");"
	
	print(comstr)
	cur.execute(comstr)
	cur.close()
	conn.commit()

#for row in cur:
#	print(row)

#	print("---")
#	print("[after]")
#	print("player ID, character ID, character_nane, HP")

#	cur.execute('select * from character;')
#	for row in cur:
#		print(row)
    
# 5.データベースの接続を切断
cur.close()
conn.close()

