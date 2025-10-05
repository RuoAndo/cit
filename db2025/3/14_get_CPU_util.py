import psutil
import pandas as pd
import time
from datetime import datetime
import os

# カレントディレクトリに保存
csv_file = os.path.join(os.getcwd(), "cpu_log.csv")

# CPUコア数に応じた項目名を生成
cpu_count = psutil.cpu_count(logical=True)
columns = ["Timestamp", "CPU_Total"] + [f"CPU_{i}" for i in range(cpu_count)]

# ===== 開始時に項目情報を表示 =====
print("ログに記録される項目名:")
for col in columns:
    print(" -", col)
print(f"\nCSVファイル: {csv_file}\n")
print("Ctrl + C で終了します...\n")

# 空のDataFrameを作り、まずヘッダーを書き込む
df = pd.DataFrame(columns=columns)
df.to_csv(csv_file, index=False, encoding="utf-8")

# ===== 1秒ごとにデータを取得して追記 =====
try:
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # CPU 全体と各コア使用率を取得
        cpu_total = psutil.cpu_percent(interval=None)
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)

        # 行データを作成
        row = [now, cpu_total] + cpu_per_core

        # CSVに追記
        pd.DataFrame([row], columns=columns).to_csv(
            csv_file, index=False, mode="a", header=False, encoding="utf-8"
        )

        # コンソールにも表示
        print(row)
        time.sleep(1)

except KeyboardInterrupt:
    print(f"\n終了しました。ログは {csv_file} に保存されています。")
