#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'TEST.db'

conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time() 
cur.execute('SELECT * FROM XY')

counter = 0
for row in cur:

	#if counter % 100 == 0:
	    # print("SELECT " + str(row))
	    
	counter = counter + 1

end = time.time() 
time_diff = end - start  
print("SELECT elapsed time:[SELECT*" + str(counter) + "]:" + str(time_diff))  

cur.close()
conn.close()