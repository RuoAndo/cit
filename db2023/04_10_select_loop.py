#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time
import datetime

import os

dbname = 'TEST.db'

os.remove('./test.log')

with open('./test.log', 'a') as f:
	print("_time, elapsed time", file=f)

while True:

	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	start = time.time() 
	cur.execute('SELECT * FROM XY')
	conn.commit()
	end = time.time() 
	time_diff = end - start  
	dt_now = datetime.datetime.now()
	
	tmpstr = str(dt_now).split(".")
	tmpstr2 = tmpstr[0].split(" ")
	
	#logstr = str(tmpstr[0]+ " " +tmpstr[1]) + "," + str(time_diff)
	logstr = str(tmpstr2[1]) + "," + str(time_diff)
	print(logstr)  

	with open('./test.log', 'a') as f:
		print(logstr, file=f)

	cur.close()
	conn.close()

	time.sleep(1)