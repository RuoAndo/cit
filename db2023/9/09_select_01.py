#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'cit-db-2023-09.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time() 
cur.execute('SELECT E.ts, C.character_name FROM event E INNER JOIN character C ON E.character_id_dst == C.character_id WHERE E.action_type == \'attack\'');

counter = 0
for row in cur:
    print(row)
    counter = counter + 1

print(counter)

cur.close()
conn.close()