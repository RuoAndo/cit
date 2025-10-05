import os
import time
from datetime import datetime

import psutil
import pandas as pd

# ===== 保存先（カレントディレクトリ） =====
csv_file = os.path.join(os.getcwd(), "cpu_log.csv")

# ===== 動的に列名を組み立て =====
cpu_count = psutil.cpu_count(logical=True)
percore_cols = [f"CPU_{i}" for i in range(cpu_count)]

# cpu_times_percent の存在する属性を確認（OS差異に対応）
times_sample = psutil.cpu_times_percent(interval=0.0)
time_cols = []
for cand in ["user", "system", "idle", "interrupt", "dpc", "iowait", "nice", "steal", "guest"]:
    if hasattr(times_sample, cand):
        time_cols.append(f"{cand.capitalize()}Pct")

# cpu_stats の属性
stats_sample = psutil.cpu_stats()
stats_cols = []
for cand, label in [
    ("ctx_switches", "CtxSwitches"),
    ("interrupts", "Interrupts"),
    ("soft_interrupts", "SoftInterrupts"),
    ("syscalls", "Syscalls"),
]:
    if hasattr(stats_sample, cand):
        stats_cols.append(label)

# 周波数
freq_cols = ["FreqCurrentMHz"]

columns = ["Timestamp", "CPU_Total"] + percore_cols + time_cols + stats_cols + freq_cols

# ===== 項目名を表示 =====
print("ログに記録される項目名:")
for col in columns:
    print(" -", col)
print(f"\nCSVファイル: {csv_file}")
print("Ctrl + C で終了します...\n")

# ===== CSVヘッダーを書き込み =====
pd.DataFrame(columns=columns).to_csv(csv_file, index=False, encoding="utf-8")

# 初期化（以降の percent 計測が安定するように）
psutil.cpu_percent(interval=0.0, percpu=True)
psutil.cpu_times_percent(interval=0.0)

try:
    while True:
        # 1秒計測（この呼び出し自体が1秒ブロッキング）
        per_core = psutil.cpu_percent(interval=1.0, percpu=True)
        total = sum(per_core) / len(per_core) if per_core else psutil.cpu_percent(interval=None)

        # 直後にその他情報を取得
        t = psutil.cpu_times_percent(interval=0.0)  # %配分（直近）
        s = psutil.cpu_stats()                      # 累積カウント系
        f = psutil.cpu_freq()                       # MHz

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [now, total] + per_core

        # times_percent を列順に格納
        for col in time_cols:
            name = col.replace("Pct", "").lower()     # user/system/idle/interrupt/dpc...
            val = getattr(t, name, None)
            row.append(round(val, 2) if isinstance(val, (int, float)) else "")

        # stats
        for col in stats_cols:
            # 対応する psutil 名に逆変換
            mapping = {
                "CtxSwitches": "ctx_switches",
                "Interrupts": "interrupts",
                "SoftInterrupts": "soft_interrupts",
                "Syscalls": "syscalls",
            }
            val = getattr(s, mapping[col], None)
            row.append(int(val) if isinstance(val, (int, float)) else "")

        # freq (current MHz)
        row.append(round(f.current, 2) if f and getattr(f, "current", None) is not None else "")

        # 追記
        pd.DataFrame([row], columns=columns).to_csv(
            csv_file, index=False, mode="a", header=False, encoding="utf-8"
        )

        # 画面表示（簡易）
        print(row)

except KeyboardInterrupt:
    print(f"\n終了しました。ログは {csv_file} に保存されています。")
