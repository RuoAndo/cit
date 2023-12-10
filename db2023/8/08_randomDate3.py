import datetime
import random

def generateRandomDateTime():
    today  = datetime.datetime.now()
    dates = [(today + datetime.timedelta(days=i))for i in range(0, 5)]
    t = datetime.time(hour=random.randint(8, 15), minute=random.randint(0, 59), second=random.randint(0, 59))
    random_date = random.choice(dates)
    return datetime.datetime.combine(random_date, t)

print(generateRandomDateTime())