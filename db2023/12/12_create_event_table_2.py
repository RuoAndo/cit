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

dbname = 'cit-db-2023-12.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

try:
	comstr1 = "drop table event;"
	cur.execute(comstr1)
	print("table dropped.")

except:
	pass

comstr2 = "create table event (event_id INTEGER PRIMARY KEY, ts TIMESTAMP, character_id INTEGER, player_id INTEGER, character_id_dst INTEGER, player_id_dst INTEGER, action_type VARCHAR(20), action_value INTEGER);"

print(comstr2)

cur.execute(comstr2)
#conn.commit()

counter = 0

for number in range(1000):

	playerID_src  = random.randrange(1, 30, 1)
	characterID_src  = random.randrange(1, 100, 1)
	
	playerID_dst  = random.randrange(1, 30, 1)
	characterID_dst  = random.randrange(1, 100, 1)
	
	l = ['attack', 'recover']
	l_weight = [2,1]
	action_name = random.choices(l, weights=l_weight)
	
	action_value = random.randrange(1, 30, 1)

	comstr3 = "select * from character where character_id =" + str(characterID_dst) + ";"
	print(comstr3)

	cur3 = conn.cursor()
	cur3.execute(comstr3)

	for row in cur3:
		print(row)

	HP = row[3]
	MP = row[4]
	EXP = row[5]

	if action_name[0] == 'attack':
		print("= ATTACK Event =")
		
		HP = HP - action_value
		comstr4 = "update character set HP = " + str(HP) + " where character_id = " + str(characterID_dst) + ";"
		print("attack dst: " + comstr4)
		cur4 = conn.cursor()
		cur4.execute(comstr4)
		conn.commit()
		print("\n")
	
	if action_name[0] == 'recover':
			print("= RECOVER Event =")

			# rocover dst
			HP = HP + action_value
			comstr4 = "update character set HP = " + str(HP) + " where character_id = " + str(characterID_dst) + ";"
			print("recover dst : " + comstr4)
			cur4 = conn.cursor()
			cur4.execute(comstr4)
			conn.commit()
		
			# rocover src
			comstr4 = "select * from character where character_id =" + str(characterID_src) + ";"
			#print(" -> RECOVER : " + comstr4)

			cur4 = conn.cursor()
			cur4.execute(comstr4)
			
			for row in cur4:
				print(row)
			
			HP = row[3]
			MP = row[4]
			EXP = row[5]
			
			MP = MP - 10
			
			comstr4 = "update character set MP = " + str(MP) + " where character_id = " + str(characterID_src) + ";"
			cur4 = conn.cursor()
			cur4.execute(comstr4)
			conn.commit()
			print("recover src : " + comstr4)
			
			print("\n")
	
	
	#HP  = random.randrange(1, 100, 1)
	#MP  = random.randrange(1, 100, 1)
	#EXP  = random.randrange(1, 100, 1)

	TS = generateRandomDateTime()

	comstr = "insert into event (ts, character_id, player_id, character_id_dst, player_id_dst, action_value, action_type ) values(" + "'" + str(TS) + "'" + "," + str(characterID_src) + "," + str(playerID_src) + "," + str(characterID_dst) + "," + str(playerID_dst) + "," + "\"" + str(action_name[0]) + "\"" + "," + str(action_value) + ");"

	#print(comstr)
	#comstr = "insert into event (event_id, ts, character_id, player_id, character_id_dst, player_id_dst, action_value, action_type ) values(" +  str(number) + "," + "'" + str(TS) + "'" + "," + str(characterID_src) + "," + str(playerID_src) + "," + str(characterID_dst) + "," + str(playerID_dst) + "," + "\"" + str(action_name[0]) + "\"" + "," + str(action_value) + ");"
		
	#print(comstr)
	cur.execute(comstr)

	conn.commit()

	if(counter%100==0):
		print(comstr)
		dt_now = datetime.datetime.now()
		print("[" + str(dt_now) + "] " + "INSERTED: " + str(counter) + "(/1000)")

	counter = counter + 1

#cur = conn.cursor()
#cur.execute('select * from event limit 10')

#for row in cur:
#	print(row)

cur.close()
conn.close()