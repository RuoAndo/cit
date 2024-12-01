#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

import string

# the number of characters: 100
# the number of players: 30

LETTERS = string.ascii_letters
#LETTERS = string.ascii_letters + string.digits + string.punctuation

def get_random_string(num):

    random_letters = random.choices(LETTERS, k=num)
    random_string = ''.join(random_letters)
    return random_string

dbname = 'cit-db-2024-07.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

try:
	comstr1 = "drop table player;"
	cur.execute(comstr1)

except:
	pass

#comstr2 = "create table player (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));"
comstr2 = "create table player (player_id INTEGER, first_name VARCHAR(20), last_name VARCHAR(20), points INTEGER, player_rank VARCHAR(20));"
# 3.テーブルに人名データを登録する
cur.execute(comstr2)

for number in range(100):

	fname = get_random_string(5)
	#print(fname)

	lname = get_random_string(5)
	#print(lname)

	rank = ''.join(random.choices(string.ascii_uppercase, k=1))
	#print(rank)

	point  = random.randrange(1, 100, 1)
	#print(point)

	comstr = "insert into player (player_id, first_name, last_name, points, player_rank) values('" + str(number) + "','" + fname + "','" + lname + "','" + str(point) + "','" + rank + "');"
	print(comstr)

	cur.execute(comstr)
	conn.commit()

	cur = conn.cursor()
	cur.execute('select * from player limit 10')

for row in cur:
	print(row)

cur.close()
conn.close()