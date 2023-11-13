import pandas as pd

a1 = pd.read_csv("access_log_tmp_1.csv")
a1.head

a2 = pd.read_csv("access_log_tmp_2.csv")
a2.head

a12 = pd.concat([a1, a2], ignore_index=True)

a12.head
