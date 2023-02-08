#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time
import datetime

dbname = 'cit-7.db'
# 1.データベースに接続

i = 0

while i < 500:

	conn = sqlite3.connect(dbname)
	print("STATUS:")
	
	# 2.sqliteを操作するカーソルオブジェクトを作成
	cur = conn.cursor()
	cur.execute('select * from player inner join character on character.person_id = player.person_id;')

	#(1, 'taro', 'yamada', 0, 'D', 1, 1, 'doraemon', -267, 10, 0)
	#(1, 'taro', 'yamada', 0, 'D', 1, 2, 'akinator', -289, 5, 0)
	#(2, 'hanako', 'sato', 0, 'D', 2, 2, 'akinator', -289, 5, 0)

	now = datetime.datetime.now()
	print(now)
	for row in cur:
		print(row)	

	cur.close()

	cur2 = conn.cursor()
	cur2.execute('select * from character;')
	for row2 in cur2:
		#print("test"+str(row2))
		playerID = row2[0]
		charaID = row2[1]
		charaName = row2[2]
	
		recover = random.randint(0, 10)	
		currentHP = row2[3]
		nextHP = currentHP + recover
		
		comstr = "update character set HP=" + str(nextHP) + " where character_id = " + str(charaID) + " and person_id=" + str(playerID) + ";"
		print(comstr)
		cur3 = conn.cursor()
		cur3.execute(comstr)
		
		recover = random.randint(0, 50)
		currentEXP = row2[5]
		nextEXP = currentEXP + recover
		
		comstr = "update character set EXP=" + str(nextEXP) + " where character_id = " + str(charaID) + " and person_id=" + str(playerID) + ";"
		print(comstr)
		cur3 = conn.cursor()
		cur3.execute(comstr)
		cur3.close()
	
	conn.commit()
	cur2.close()
	
	print("--- ---")

	conn.close()

	time.sleep(5)
    
# 5.データベースの接続を切断
#cur.close()
#cur2.close()
#cur3.close
#conn.close()

