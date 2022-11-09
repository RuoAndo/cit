#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルのCreate文を実行(例ではpersonsテーブルを作成)
cur.execute(
    'CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')

# 4.データベースに情報をコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()