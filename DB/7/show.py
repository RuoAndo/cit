#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.playerテーブルを見る
cur.execute('select * from player;')
for row in cur:
    print(row)
    
# 4.characterテーブルを見る
cur.execute('select * from character;')
for row in cur:
    print(row)
    
# 5.データベースの接続を切断
cur.close()
conn.close()

