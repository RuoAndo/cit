import random


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

dbname = 'cit-db-2023-07.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

try:
	comstr1 = "drop table character;"
	cur.execute(comstr1)

except:
	pass


#comstr2 = "create table character (player_id INTEGER PRIMARY KEY AUTOINCREMENT, character_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);"
comstr2 = "create table character (character_id INTEGER, player_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);"

cur.execute(comstr2)
conn.commit()


for number in range(1000):

	l = ['doraemon', 'akinator', 'golgo', 'begita', 'bikkuriko']
	point  = random.randrange(0, 5, 1)
	#print(str(point) + "," + l[point])
	
	playerID  = random.randrange(1, 30, 1)
	
	HP  = random.randrange(1, 100, 1)
	MP  = random.randrange(1, 100, 1)
	EXP  = random.randrange(1, 100, 1)

	comstr = "insert into character (character_id, player_id, character_name, HP, MP, EXP) values(" +  str(number) + "," + str(playerID) + ",'" + l[point] + "'," + str(HP) + "," + str(MP) + "," + str(EXP) + ");"
	print(comstr)
	cur.execute(comstr)

	conn.commit()



cur = conn.cursor()
cur.execute('select * from character limit 10')

for row in cur:
	print(row)

cur.close()
conn.close()