#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('SELECT * FROM XY')

# 取得したデータを出力
for row in cur:
    print(row)

# 4.データベースの接続を切断
cur.close()
conn.close()