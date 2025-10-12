# plot_ts_cpu_temp_swap_3d.py
# 3D散布図: X=cpu_percent, Y=temp_c(℃), Z=swap_percent(%), 色=時刻(ts)

import sqlite3
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ===== 設定 =====
DB_PATH   = "cpu_metrics.db"
TABLE     = "cpu_metrics"
START_ISO = None  # 例: "2025-10-12T00:00:00.000000Z"（Noneで全期間）
END_ISO   = None  # 例: "2025-10-12T23:59:59.999999Z"
MAX_POINTS = 20000  # 多すぎる場合は間引き
# ===============

def build_query():
    sql = f"SELECT ts, cpu_percent, temp_c, swap_percent FROM {TABLE}"
    conds, params = [], []
    if START_ISO:
        conds.append("ts >= ?"); params.append(START_ISO)
    if END_ISO:
        conds.append("ts <= ?"); params.append(END_ISO)
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY ts"
    return sql, params

def parse_ts(ts_str: str):
    # "....Z" → "+00:00" にしてISOパース
    if ts_str.endswith("Z"):
        ts_str = ts_str[:-1] + "+00:00"
    return datetime.fromisoformat(ts_str).astimezone(timezone.utc)

def main():
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = con.cursor()
    sql, params = build_query()
    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()

    if not rows:
        raise SystemExit("データが見つかりません。期間やDBパスを確認してください。")

    t_list, x_cpu, y_temp, z_swap = [], [], [], []
    for ts, cpu, temp, swp in rows:
        if cpu is None or temp is None or swp is None:
            continue
        try:
            t = parse_ts(ts)
            x = float(cpu); y = float(temp); z = float(swp)
        except Exception:
            continue
        t_list.append(t); x_cpu.append(x); y_temp.append(y); z_swap.append(z)

    if not x_cpu:
        raise SystemExit("有効な (cpu_percent, temp_c, swap_percent) の行がありません。")

    # 点が多すぎる場合は間引き（等間隔）
    n = len(x_cpu)
    step = max(1, n // MAX_POINTS)
    t_plot  = t_list[::step]
    x_plot  = x_cpu[::step]
    y_plot  = y_temp[::step]
    z_plot  = z_swap[::step]

    # 時刻を数値化して色に使う（colormapは指定しない）
    tnum = mdates.date2num(t_plot)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(x_plot, y_plot, z_plot, c=tnum)  # デフォルトcolormapを使用

    ax.set_xlabel("cpu_percent [%]")
    ax.set_ylabel("temp_c [°C]")
    ax.set_zlabel("swap_percent [%]")
    ax.set_title("3D Scatter: cpu_percent vs temp_c vs swap_percent (color = time)")

    # カラーバー（時刻）
    cb = plt.colorbar(sc, pad=0.1)
    # カラーバーに最小・最大の日時を注記
    cb.set_label("time")
    cb.ax.set_yticklabels([])  # 目盛り文字は消して…
    # 代わりに枠外テキストで範囲を表示
    tmin, tmax = min(t_plot), max(t_plot)
    fig.text(0.92, 0.15, tmin.strftime("%Y-%m-%d\n%H:%M:%S UTC"), ha="left", va="center", fontsize=8)
    fig.text(0.92, 0.85, tmax.strftime("%Y-%m-%d\n%H:%M:%S UTC"), ha="left", va="center", fontsize=8)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
