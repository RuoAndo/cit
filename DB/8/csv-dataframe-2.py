import pandas as pd
import sys

args = sys.argv

df = pd.read_csv(args[1])
print(df)

import sqlite3
with sqlite3.connect("cit-8.db") as conn:
	df.to_sql('imdb', con=conn)
	