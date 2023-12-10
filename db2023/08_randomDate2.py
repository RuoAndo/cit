import numpy as np
import datetime

def get_random_timestamp():
    start_date = datetime.datetime.now() + datetime.timedelta(1)   # tomorrow
    start_date = start_date.replace(hour = 8, minute=0, second=0)  # set to 8 AM
    seconds_max = 7*70*60  # 8AM to 3PM is 7 hours                 # 7 hrs in seconds
    time_offset = np.random.randint(0, seconds_max)
    day_offset = np.random.choice(range(5))
    final_date = start_date + datetime.timedelta(seconds=time_offset, days=day_offset)
    return final_date

for i in range(10):
    print(datetime.datetime.strftime(get_random_timestamp(), "%Y-%m-%d %H:%M:%S"))