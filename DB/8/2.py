import time

ut = time.time()

print(ut)
# 1549281692.9876952

print(type(ut))
# <class 'float'>

import datetime

dt_now = datetime.datetime.now()

print(dt_now.strftime('%Y-%m-%d %H:%M:%S'))