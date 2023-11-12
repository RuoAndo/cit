#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'sakila_master.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time() 
cur.execute('SELECT FA.actor_id, F.title, F.description FROM film_actor FA JOIN film F ON FA.film_id = F.film_id LIMIT 5;')

for row in cur:
    print(row)

cur.close()
conn.close()