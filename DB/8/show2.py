#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.

print("player ID, character ID, character_nane, HP")

cur.execute('select * from character;')
for row in cur:
	comstr = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])
	print(comstr)

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()