# plot_3D_ctx_simple.py
# cpu_metrics.db の cpu_metrics_min から
# ts / cpu_percent / cpu_ctx_switches / temp_c を読み取り3D表示する

import sqlite3, math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from datetime import datetime, timezone

DB_PATH = "cpu_metrics.db"
TABLE   = "cpu_metrics_min"
LIMIT   = 5000  # 表示行数上限

def iso_to_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)

def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT ts, cpu_percent, cpu_ctx_switches, temp_c FROM {TABLE} ORDER BY ts ASC LIMIT {LIMIT}")
    rows = cur.fetchall()
    con.close()
    if not rows:
        print("データがありません。")
        return

    ts  = [iso_to_dt(r[0]) for r in rows]
    cpu = [float(r[1]) if r[1] is not None else math.nan for r in rows]
    ctx = [int(r[2])   if r[2] is not None else None for r in rows]
    tmp = [float(r[3]) if r[3] not in (None, "") else math.nan for r in rows]

    # 相対秒
    t0 = ts[0]
    x = [(t - t0).total_seconds() for t in ts]

    # ctx_delta
    z = [math.nan]
    for i in range(1, len(ctx)):
        if ctx[i] is None or ctx[i-1] is None:
            z.append(math.nan)
        else:
            z.append(ctx[i] - ctx[i-1])

    # プロット
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(x, cpu, z, c=tmp, s=10)
    cb = fig.colorbar(sc, shrink=0.7, pad=0.1)
    cb.set_label("温度 (°C)")
    ax.set_title("CPU負荷とコンテキストスイッチ（3D）")
    ax.set_xlabel("経過秒")
    ax.set_ylabel("CPU使用率 (%)")
    ax.set_zlabel("ctx_delta (/sec)")
    ax.view_init(elev=22, azim=-60)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
