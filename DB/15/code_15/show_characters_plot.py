#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

cur.execute("select * from character")
for row in cur.fetchall():
    print(row)
    
    print(row[3])
    print(row[5])

cur.close()
conn.close()
