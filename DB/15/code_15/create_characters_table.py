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
	comstr1 = "drop table character;"
	cur.execute(comstr1)

except:
	pass

comstr2 = "create table character (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);"

# 3.テーブルに人名データを登録する
cur.execute(comstr2)

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()
