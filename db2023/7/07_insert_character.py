#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

dbname = 'cit-db-2023-07.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

try:
	comstr1 = "drop table character;"
	cur.execute(comstr1)

except:
	pass


comstr2 = "create table character (player_id INTEGER PRIMARY KEY AUTOINCREMENT, character_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);"
cur.execute(comstr2)
conn.commit()

comstr = "insert into character (character_id, player_id, character_name, HP, MP, EXP) values(1, 1, 'doraemon', 10, 10, 0);"
cur.execute(comstr)

now = datetime.datetime.now()
print(now)

conn.commit()

cur = conn.cursor()
cur.execute('select * from character limit 10')

for row in cur:
	print(row)

cur.close()
conn.close()