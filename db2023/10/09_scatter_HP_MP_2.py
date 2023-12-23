import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./9_1.csv")

plt.scatter(df['HP'], df["MP"], label='stats')

plt.title("Status")

plt.xlabel("HP")
plt.ylabel("MP")

plt.legend()
plt.show()