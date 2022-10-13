import sqlite3
con = sqlite3.connect('sakila_master.db')
cur = con.cursor()

res = cur.execute('SELECT * FROM film LIMIT 5')
