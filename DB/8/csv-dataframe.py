import pandas as pd
import sys

args = sys.argv

df = pd.read_csv(args[1])
print(df)
