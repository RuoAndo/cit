import sqlite3
import pandas as pd

# SQLiteデータベースのパス
db_path = "cpu_log.db"  # ファイルの場所に合わせて変更

# データベースに接続
conn = sqlite3.connect(db_path)

# SQLクエリで Timestamp と CPU_0〜CPU_3 を取得
query = """
SELECT Timestamp, CPU_0, CPU_1, CPU_2, CPU_3
FROM cpu_log
ORDER BY Timestamp;
"""

# データをDataFrameに読み込み
df = pd.read_sql_query(query, conn)

# 接続を閉じる
conn.close()

# 結果を確認
print(df.head())
