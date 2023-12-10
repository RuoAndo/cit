import datetime
import random
from dateutil.relativedelta import relativedelta

def getRandamYmdFrom2019ToNowYear():
    min_year=2019
    dtMax = datetime.datetime.now()
    max_year=int(dtMax.strftime('%Y'))

    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    dt = start + (end - start) * random.random()
    print(dt.strftime('%Y-%m-%d'))
    return dt.strftime('%Y-%m-%d')
    
print(getRandamYmdFrom2019ToNowYear())