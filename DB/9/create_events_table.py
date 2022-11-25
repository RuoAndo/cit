#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

try:
	comstr = "drop table events;"
	cur.execute(comstr)

except:
	pass

comstr2 = "create table events (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), event_type VARCHAR(20), event_time VARCHAR(20));"
cur.execute(comstr2)
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()