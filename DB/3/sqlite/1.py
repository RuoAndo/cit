import sqlite3
con = sqlite3.connect('sakila_master.db')
cur = con.cursor()

for row in cur.execute('SELECT * FROM film LIMIT 5'):
	print(row)