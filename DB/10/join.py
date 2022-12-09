#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

cur.execute("select * from player inner join character on character.person_id = player.person_id;")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
