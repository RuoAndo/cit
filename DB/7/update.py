#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

HP = random.randint(0, 20)
MP = random.randint(0, 20)
comstr = "update character set HP=" + str(HP) + ", MP=" + str(MP) + ", EXP=5 where character_id = 1;"

# 3.テーブルに人名データを登録する
cur.execute(comstr)

HP = random.randint(0, 20)
MP = random.randint(0, 20)
comstr = "update character set HP=" + str(HP) + ", MP=" + str(MP) + ", EXP=5 where character_id = 2;"

cur.execute(comstr)


# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()