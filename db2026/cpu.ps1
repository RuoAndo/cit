import psutil
import sqlite3
import time
from datetime import datetime

DB_FILE = "cpu_usage.db"

# SQLiteへ接続
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS cpu_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_percent REAL NOT NULL
)
""")

conn.commit()

try:
    while True:
        # 1秒間のCPU使用率
        usage = psutil.cpu_percent(interval=1)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # SQLiteへ保存
        cur.execute(
            """
            INSERT INTO cpu_usage (
                timestamp,
                cpu_percent
            )
            VALUES (?, ?)
            """,
            (timestamp, usage)
        )

        conn.commit()

        print(timestamp, f"CPU: {usage:.1f}%")

except KeyboardInterrupt:
    print("終了します。")

finally:
    conn.close()