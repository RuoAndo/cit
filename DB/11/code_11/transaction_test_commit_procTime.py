#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time

dbname = 'cit-7.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

print("transaction test")
print("player ID, character ID, character_nane, HP")

cur.execute('select * from character;')

print("")
print("transaction start:")
print("")

time_sta = time.time()

for row in cur:
	cur2 = conn.cursor()
	print(row)
	#strhp = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])
	#print(strhp)

	charaID = row[1];

	cur2.execute('BEGIN IMMEDIATE TRANSACTION test;')
	cur2.execute('select * from character;')

	comstr = "update character set HP=0" + " where character_id = " + str(charaID) + ";"
	print("- " + comstr)
	cur2.execute(comstr)
	cur2.execute('COMMIT;')

	cur2.close()	
	#conn.commit()		
	print("- transaction committed")
	print("")

print("transaction end:")
time_end = time.time()
# åoâﬂéûä‘ÅiïbÅj
tim = time_end- time_sta
print("")
print("elapsed time:" + str(tim))

print("")
print("result:")

cur.execute('select * from character;')
for row in cur:
	print(row)

cur.close()
conn.close()

