import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.family'] = ['Meiryo', 'Yu Gothic', 'MS Gothic']  # いずれかが入っていればOK


# === SQLiteデータベースへの接続 ===
db_path = "cpu_log.db"  # ファイルの場所に合わせて変更
conn = sqlite3.connect(db_path)

# === データを取得 ===
query = """
SELECT Timestamp, CPU_0, CPU_1, CPU_2, CPU_3
FROM cpu_log
ORDER BY Timestamp;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# === Timestampを時系列データに変換 ===
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# === グラフを作成 ===
plt.figure(figsize=(12, 6))
plt.plot(df["Timestamp"], df["CPU_0"], label="CPU_0")
plt.plot(df["Timestamp"], df["CPU_1"], label="CPU_1")
plt.plot(df["Timestamp"], df["CPU_2"], label="CPU_2")
plt.plot(df["Timestamp"], df["CPU_3"], label="CPU_3")

# === タイトル・ラベル・凡例 ===
plt.title("CPUコアごとの使用率推移", fontsize=14)
plt.xlabel("時刻", fontsize=12)
plt.ylabel("CPU使用率(%)", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
