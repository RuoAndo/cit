#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time
import datetime

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

# 3.

print("[before]")
print("player ID, character ID, character_nane, HP")

cur.execute('select * from character;')

for row in cur:

	cur2 = conn.cursor()

	print(row)
	strhp = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])
	#print(strhp)

	dt_now = datetime.datetime.now()
	timestr = dt_now.strftime('%Y-%m-%d %H:%M:%S')

	print("---")
	print("event: attack(HP) at: " + timestr + " to: " + str(row[2]))
	print("---")

	cur2 = conn.cursor()
	eventstr = "insert into events (person_id, character_id, character_name, event_type, event_time) values(" + str(row[0]) + "," + str(row[1]) + ",'" +  str(row[2]) + "'," + "'attack'" + ",'" +  timestr + "');"
	print(eventstr)
	cur2.execute(eventstr)
	cur2.close()

	cur3 = conn.cursor()
	charaID = row[1];
	damage = random.randint(0, 5)	
	currentHP = row[3]
	nextHP = currentHP - damage

	comstr = "update character set HP=" + str(nextHP) + " where character_id = " + str(charaID) + ";"
	#print(comstr)
	cur3.execute(comstr)
	cur3.close()
	
conn.commit()

print("---")
print("[after]")
print("player ID, character ID, character_nane, HP")

cur.execute('select * from character;')
for row in cur:
    print(row)
    

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()

