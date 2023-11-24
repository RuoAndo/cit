#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime


import string

LETTERS = string.ascii_letters
#LETTERS = string.ascii_letters + string.digits + string.punctuation

def get_random_string(num):

    random_letters = random.choices(LETTERS, k=num)
    random_string = ''.join(random_letters)
    return random_string

fname = get_random_string(5)
print(fname)

lname = get_random_string(5)
print(lname)

rank = ''.join(random.choices(string.ascii_uppercase, k=1))
print(rank)

point  = random.randrange(1, 100, 1)
print(point)

dbname = 'cit-db-2023-07.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

comstr = "insert into player (fname, lname, points, rank) values('" + fname + "','" + lname + "','" + str(point) + "','" + rank + "');"
print(comstr)

cur.execute(comstr)

conn.commit()

cur = conn.cursor()
cur.execute('select * from player')

for row in cur:
	print(row)

cur.close()
conn.close()