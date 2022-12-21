#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time

import json

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

i = 0

while i < 500:

	# 2.sqliteを操作するカーソルオブジェクトを作成
	cur = conn.cursor()
	
	#cur.execute('.mode json')
	cur.execute('select * from player inner join character on character.person_id = player.person_id;')

	print("SQL: select * from player inner join character on character.person_id = player.person_id;")

	#(1, 'taro', 'yamada', 0, 'D', 1, 1, 'doraemon', -267, 10, 0)
	#(1, 'taro', 'yamada', 0, 'D', 1, 2, 'akinator', -289, 5, 0)
	#(2, 'hanako', 'sato', 0, 'D', 2, 2, 'akinator', -289, 5, 0)

	list1 = []

	for row in cur:
		d = {}
		list2 = []
			
		#print(row)
		
		#print(str(row[0]))
		d = {}
		d["player_id"] = str(row[0])
		list2.append(d)
		
		#print(str(row[0]))
		d = {}
		d["first_name"] = str(row[1])
		list2.append(d)
		
		d = {}
		d["last_name"] = str(row[2])
		list2.append(d)
		
		d = {}
		d["point"] = str(row[3])
		list2.append(d)
		
		d = {}
		d["rank"] = str(row[4])
		list2.append(d)
	
		d = {}
		d["character_id"] = str(row[5])
		list2.append(d)
		
		d = {}
		d["player_id"] = str(row[6])
		list2.append(d)
		
		d = {}
		d["character_name"] = str(row[7])
		list2.append(d)
		
		d = {}
		d["HP"] = str(row[8])
		list2.append(d)
		
		d = {}
		d["MP"] = str(row[9])
		list2.append(d)
		
		d = {}
		d["EXP"] = str(row[10])
		list2.append(d)
	
		#print(list2)
		#list2.clear()
	
		#print("---")
		list1.append(list2)
	
	print(list1)
	
	print("-----")
	
	time.sleep(2)
    
# 5.データベースの接続を切断
cur.close()
conn.close()

