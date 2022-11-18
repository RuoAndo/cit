# -*- coding: Shift-JIS -*-

import time
import random
import datetime


for number in range(10):

	dt_now = datetime.datetime.now()
	print(dt_now.strftime('%Y-%m-%d %H:%M:%S'))

	waitsec=random.randint(1,5)
	time.sleep(waitsec)
