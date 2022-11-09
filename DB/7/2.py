#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルに人名データを登録する
# 例では、personsテーブルのnameカラムに「Sato」「Suzuki」「Takahashi」というデータを登録
cur.execute('INSERT INTO persons(name) values("Sato")')

cur.execute('INSERT INTO persons(name) values("Suzuki")')

cur.execute('INSERT INTO persons(name) values("Takahashi")')

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()


