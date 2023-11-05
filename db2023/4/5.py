#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time()  
cur.execute('SELECT * FROM XY')
end = time.time()  

# 取得したデータを出力
#for row in cur:
#    print(row)

time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する
print(time_diff)  # 処理にかかった時間データを使用

# 4.データベースの接続を切断
cur.close()
conn.close()