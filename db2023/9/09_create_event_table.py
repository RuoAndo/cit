import sqlite3
import random

import datetime
import random

def generateRandomDateTime():
    today  = datetime.datetime.now()
    dates = [(today + datetime.timedelta(days=i))for i in range(0, 5)]
    t = datetime.time(hour=random.randint(8, 15), minute=random.randint(0, 59), second=random.randint(0, 59))
    random_date = random.choice(dates)
    return datetime.datetime.combine(random_date, t)

dbname = 'cit-db-2023-09.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

try:
	comstr1 = "drop table event;"
	cur.execute(comstr1)

except:
	pass

comstr2 = "create table event (ts TIMESTAMP, character_id_src INTEGER, player_id_src INTEGER, character_id_dst INTEGER, player_id_dst INTEGER, action_type VARCHAR(20));"

cur.execute(comstr2)
conn.commit()

counter = 0

for number in range(1000):

	#l = ['doraemon', 'akinator', 'golgo', 'begita', 'bikkuriko']
	#l_weight = [10, 1, 1, 1, 1]
	#character_name = random.choices(l, weights=l_weight)
	
	playerID_src  = random.randrange(1, 30, 1)
	characterID_src  = random.randrange(1, 100, 1)
	
	playerID_dst  = random.randrange(1, 30, 1)
	characterID_dst  = random.randrange(1, 100, 1)
	
	l = ['attack', 'recover']
	l_weight = [2,1]
	action_name = random.choices(l, weights=l_weight)
	
	#HP  = random.randrange(1, 100, 1)
	#MP  = random.randrange(1, 100, 1)
	#EXP  = random.randrange(1, 100, 1)

	TS = generateRandomDateTime()
	#print(TS)
	#print(action_name)

	comstr = "insert into event (ts, character_id_src, player_id_src, character_id_dst, player_id_dst, action_type ) values(" +  "'" + str(TS) + "'" + "," + str(characterID_src) + "," + str(playerID_src) + "," + str(characterID_dst) + "," + str(playerID_dst) + "," + "\"" + str(action_name[0]) + "\"" + ");"
	#print(comstr)
	cur.execute(comstr)

	conn.commit()

	if(counter%100==0):
		print(comstr)
		dt_now = datetime.datetime.now()
		print("[" + str(dt_now) + "] " + "INSERTED: " + str(counter) + "(/1000)")

	counter = counter + 1

cur = conn.cursor()
cur.execute('select * from event limit 10')

for row in cur:
	print(row)

cur.close()
conn.close()