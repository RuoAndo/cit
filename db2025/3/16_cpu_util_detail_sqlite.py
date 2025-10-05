import os
import time
import sqlite3
from datetime import datetime
import psutil

# ===== SQLite データベースファイル（カレントディレクトリ） =====
db_file = os.path.join(os.getcwd(), "cpu_log.db")

# ===== DB 接続 & テーブル作成 =====
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# CPUコア数
cpu_count = psutil.cpu_count(logical=True)

# 動的にカラムを作成
columns = ["Timestamp TEXT", "CPU_Total REAL"]
columns += [f"CPU_{i} REAL" for i in range(cpu_count)]
columns += ["UserPct REAL", "SystemPct REAL", "IdlePct REAL", "InterruptPct REAL", "DpcPct REAL"]
columns += ["CtxSwitches INTEGER", "Interrupts INTEGER", "SoftInterrupts INTEGER", "Syscalls INTEGER"]
columns += ["FreqCurrentMHz REAL"]

# テーブル作成（既に存在すれば無視）
cur.execute(f"CREATE TABLE IF NOT EXISTS cpu_log ({', '.join(columns)})")
conn.commit()

print("記録される項目:")
for c in columns:
    print(" -", c.split()[0])
print(f"\nSQLite DB: {db_file}")
print("Ctrl + C で終了します...\n")

# 初期化
psutil.cpu_percent(interval=0.0, percpu=True)
psutil.cpu_times_percent(interval=0.0)

try:
    while True:
        # 1秒間隔でCPU使用率を取得
        per_core = psutil.cpu_percent(interval=1.0, percpu=True)
        total = sum(per_core) / len(per_core)

        # 詳細情報
        t = psutil.cpu_times_percent(interval=0.0)
        s = psutil.cpu_stats()
        f = psutil.cpu_freq()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            now, total, *per_core,
            getattr(t, "user", None),
            getattr(t, "system", None),
            getattr(t, "idle", None),
            getattr(t, "interrupt", None),
            getattr(t, "dpc", None),
            getattr(s, "ctx_switches", None),
            getattr(s, "interrupts", None),
            getattr(s, "soft_interrupts", None),
            getattr(s, "syscalls", None),
            f.current if f else None
        ]

        # DBに書き込み
        placeholders = ",".join("?" * len(row))
        cur.execute(f"INSERT INTO cpu_log VALUES ({placeholders})", row)
        conn.commit()

        print(row)

except KeyboardInterrupt:
    print(f"\n終了しました。ログは {db_file} に保存されています。")
    conn.close()
