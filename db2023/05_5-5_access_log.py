import re

PATTERN =r'[0-9]+(?:\.[0-9]+){3}'

PATTERN2 = r'\[.*\]' 

ipaddr = []
t = []

with open('./access_log.txt') as f:
	for line in f:
		#print(line)
       
		ipList = re.findall( PATTERN, line )
		for ip in ipList:
			#print(ip)
			ipaddr.append(str(ip))
		
		timestamp = re.findall(PATTERN2, line)
		for ts in timestamp:
			try:
				t.append(str(ts))
			except:
				print("pass")
			
import sqlite3

dbname = 'TEST2.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sql = """DROP TABLE IF EXISTS ACCESS"""
conn.execute(sql)

cur.execute(
    'CREATE TABLE ACCESS(id INTEGER PRIMARY KEY AUTOINCREMENT, ts STRING, ip STRING)')

conn.commit()

cur.close()
conn.close()
		
conn = sqlite3.connect(dbname)
cur = conn.cursor()

counter = 0
for j in ipaddr:

	try:
		#print(t[counter]+","+j)
		commstr = 'INSERT INTO ACCESS values(' + str(counter) + ',"' + t[counter] + '","' + str(j) + '");'
		#print(commstr)
		cur.execute(commstr)
		conn.commit()	
		
		if(counter % 100 == 0):
			print(commstr)
	
	except:
		pass
	
	counter = counter + 1

cur.close()
conn.close()