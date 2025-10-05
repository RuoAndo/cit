import sqlite3
import pandas as pd

conn = sqlite3.connect("cpu_log.db")
df = pd.read_sql("SELECT * FROM cpu_log", conn)
print(df.head())
