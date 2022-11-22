import pandas as pd
import sys

args = sys.argv

df = pd.read_csv(args[1])
print(df)

import sqlite3

with sqlite3.connect("cit-8.db") as conn:
	sql = """DROP TABLE imdb"""
	conn.execute(sql) 
	#conn.close()      

with sqlite3.connect("cit-8.db") as conn:
	df.to_sql('imdb', con=conn)
	
with sqlite3.connect("cit-8.db") as conn:
    cur = conn.cursor()
    cur.execute( "select * from imdb LIMIT 5" )
    print(cur.fetchall())