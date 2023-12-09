import random

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

import datetime
import random

def generateRandomDateTime():
    today  = datetime.datetime.now()
    dates = [(today + datetime.timedelta(days=i))for i in range(0, 5)]
    t = datetime.time(hour=random.randint(8, 15), minute=random.randint(0, 59), second=random.randint(0, 59))
    random_date = random.choice(dates)
    return datetime.datetime.combine(random_date, t)

dbname = 'cit-db-2023-08.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

try:
	comstr1 = "drop table event;"
	cur.execute(comstr1)

except:
	pass

comstr2 = "create table event (ts TIMESTAMP, character_id INTEGER, player_id INTEGER, character_name VARCHAR(20), character_id_attacked INTEGER);"

cur.execute(comstr2)
conn.commit()

counter = 0

for number in range(4000):

	#l = ['doraemon', 'akinator', 'golgo', 'begita', 'bikkuriko']
	#l_weight = [10, 1, 1, 1, 1]
	#character_name = random.choices(l, weights=l_weight)
	
	playerID  = random.randrange(1, 30, 1)
	characterID  = random.randrange(1, 100, 1)
	
	characterID_attacked = random.randrange(1, 100, 1)
	
	HP  = random.randrange(1, 100, 1)
	#MP  = random.randrange(1, 100, 1)
	#EXP  = random.randrange(1, 100, 1)

	TS = generateRandomDateTime()
	#print(TS)

	comstr = "insert into event (ts, character_id, player_id, character_id_attacked) values(" +  "'" + str(TS) + "'" + "," + str(characterID) + "," + str(playerID) + "," + str(characterID_attacked) + ");"
	#print(comstr)
	cur.execute(comstr)

	conn.commit()

	if(counter%1000==0):
		dt_now = datetime.datetime.now()
		print("[" + str(dt_now) + "] " + "INSERTED: " + str(counter) + "(4000)")

	counter = counter + 1

cur = conn.cursor()
cur.execute('select * from event limit 10')

for row in cur:
	print(row)

cur.close()
conn.close()