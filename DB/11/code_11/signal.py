def func(num, frame):
    print (num, str(frame))

signal.signal(signal.SIGINT, func)
for i in range(100):
   sleep(10)