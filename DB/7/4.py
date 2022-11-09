#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

#データベースに接続する
conn = sqlite3.connect('TEST.db')
c = conn.cursor()

sql = """DROP TABLE IF EXISTS persons"""

conn.execute(sql)

#保存（コミット）する
conn.commit()