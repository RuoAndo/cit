#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

comstr = "insert into player (fname, lname, points, rank) values('taro', 'yamada', '0', 'D');"
cur.execute(comstr)

comstr = "insert into player (fname, lname, points, rank) values('hanako', 'sato', '0', 'D');"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1, 1, 'doraemon', 10, 10, 0);"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1, 2, 'akinator', 15, 5, 0);"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(2, 2, 'akinator', 15, 5, 0);"
cur.execute(comstr)

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()