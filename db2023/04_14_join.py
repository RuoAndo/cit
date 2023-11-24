#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'sakila_master.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time() 
cur.execute('SELECT A.first_name, A.last_name, FA.actor_id, FA.film_id, count(*) FROM actor A JOIN film_actor FA ON A.actor_id = FA.actor_id GROUP BY A.first_name, A.last_name limit 5;')

for row in cur:
    print(row)

cur.close()
conn.close()