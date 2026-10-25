import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db = "02_cpu_usage.db"

print("[1/6] SQLiteデータベースへ接続中...")

try:
    conn = sqlite3.connect(db)
    print("[OK] 接続完了")
except Exception as e:
    print("[ERROR] DB接続失敗:", e)
    raise

print()

# --------------------------------------------------
# データ読み込み
# --------------------------------------------------

print("[2/6] cpu_usage テーブルを読み込み中...")

try:
    df = pd.read_sql_query(
        """
        SELECT *
        FROM cpu_usage
        ORDER BY timestamp
        """,
        conn
    )

    print(f"[OK] 読み込み完了: {len(df)} 件")

except Exception as e:
    print("[ERROR] 読み込み失敗:", e)
    conn.close()
    raise

conn.close()

print("[OK] SQLite接続を終了しました")
print()

# --------------------------------------------------
# 日時変換
# --------------------------------------------------

print("[3/6] timestampを日時型へ変換中...")

try:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print("[OK] 日時変換完了")
except Exception as e:
    print("[ERROR] 日時変換失敗:", e)
    raise

print()

# --------------------------------------------------
# 必要な列を確認
# --------------------------------------------------

print("[4/6] 必要な列を確認中...")

required_columns = [
    "timestamp",
    "cpu_percent",
    "user_percent",
    "privileged_percent",
    "idle_percent",
    "interrupt_percent",
    "current_clock_mhz"
]

for col in required_columns:
    if col in df.columns:
        print(f"[OK] {col}")
    else:
        print(f"[ERROR] {col} がありません")
        raise KeyError(col)

print()

# --------------------------------------------------
# グラフ作成
# --------------------------------------------------

print("[5/6] グラフを作成中...")

fig, axes = plt.subplots(
    3,
    2,
    figsize=(16, 12)
)

plots = [
    ("cpu_percent", "CPU Usage", "Percent"),
    ("user_percent", "User CPU", "Percent"),
    ("privileged_percent", "Kernel CPU", "Percent"),
    ("idle_percent", "CPU Idle", "Percent"),
    ("interrupt_percent", "CPU Interrupt", "Percent"),
    ("current_clock_mhz", "Current CPU Clock", "MHz")
]

for i, (column, title, ylabel) in enumerate(plots, start=1):

    print(
        f"  [{i}/6] {title} を作成中...",
        end=""
    )

    row = (i - 1) // 2
    col = (i - 1) % 2

    ax = axes[row, col]

    ax.plot(
        df["timestamp"],
        df[column]
    )

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Time")
    ax.grid(True)

    ax.tick_params(
        axis="x",
        rotation=30
    )

    print(" 完了")

print()
print("[OK] 全グラフ作成完了")

# --------------------------------------------------
# 保存
# --------------------------------------------------

print()
print("[6/6] PNGファイルへ保存中...")

output_file = "cpu_monitor_2col.png"

try:

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"[OK] 保存完了: {output_file}")

except Exception as e:

    print("[ERROR] PNG保存失敗:", e)
    raise

print()
print("====================================")
print("すべての処理が完了しました")
print("====================================")
print()

plt.show()