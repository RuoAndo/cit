# plot_3d_by_columns_black.py
# SQLiteから3列を取り出し、各軸を列名でラベル付けして黒い点で3D散布図を描く

# ===== 日本語文字化け・豆腐対策ヘッダ =====
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import matplotlib
from matplotlib import font_manager
matplotlib.rcParams["axes.unicode_minus"] = False
_JP_FONT_CANDIDATES = ["Yu Gothic","Meiryo","MS PGothic","MS Gothic",
                       "Noto Sans CJK JP","Noto Sans JP","IPAGothic","TakaoPGothic"]
_LOCAL_FONT_FILE = "NotoSansCJKjp-Regular.otf"; _LOCAL_FONT_NAME = "Noto Sans CJK JP"
def _choose_jp_font():
    if os.path.exists(_LOCAL_FONT_FILE):
        try:
            font_manager.fontManager.addfont(_LOCAL_FONT_FILE)
            return _LOCAL_FONT_NAME
        except Exception: pass
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in _JP_FONT_CANDIDATES:
        if name in installed: return name
    return None
_f = _choose_jp_font()
if _f: matplotlib.rcParams["font.family"] = [_f]
# =========================================

import argparse
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

def main():
    ap = argparse.ArgumentParser(description="3列を黒点で3Dプロット（軸=列名）")
    ap.add_argument("--db", default="cpu_metrics.db", help="SQLite DBパス")
    ap.add_argument("--table", default="cpu_metrics_min", help="テーブル名")
    ap.add_argument("--cols", default="cpu_percent,cpu_ctx_switches,temp_c",
                    help="カンマ区切りの3列名（例: cpu_percent,mem_shared,temp_c）")
    ap.add_argument("--limit", type=int, default=5000, help="取得上限（時系列昇順）")
    ap.add_argument("--out", default="plot_3d_black.png", help="保存PNGファイル名")
    args = ap.parse_args()

    cols = [c.strip() for c in args.cols.split(",")]
    if len(cols) != 3:
        raise SystemExit(" --cols は3列を指定してください（例: cpu_percent,mem_shared,temp_c）")

    # データ取得
    con = sqlite3.connect(args.db)
    cur = con.cursor()
    cur.execute(f"PRAGMA table_info({args.table})")
    existing = {r[1] for r in cur.fetchall()}
    for c in cols:
        if c not in existing:
            con.close()
            raise SystemExit(f"列が見つかりません: {c} （テーブル: {args.table}）")

    has_ts = "ts" in existing
    if has_ts:
        sql = f"SELECT ts, {cols[0]}, {cols[1]}, {cols[2]} FROM {args.table} ORDER BY ts ASC LIMIT ?"
    else:
        sql = f"SELECT {cols[0]}, {cols[1]}, {cols[2]} FROM {args.table} LIMIT ?"
    df = pd.read_sql_query(sql, con, params=(args.limit,))
    con.close()
    if df.empty:
        raise SystemExit("データがありません。")

    if has_ts:
        df.columns = ["ts", cols[0], cols[1], cols[2]]
        df = df.dropna(subset=[cols[0], cols[1], cols[2]])
        X = df[[cols[0], cols[1], cols[2]]].to_numpy(dtype=float)
    else:
        df = df.dropna()
        X = df[[cols[0], cols[1], cols[2]]].to_numpy(dtype=float)

    if X.size == 0:
        raise SystemExit("有効な数値データがありません。")

    # 黒い点で3D散布
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(X[:,0], X[:,1], X[:,2], s=14, c="black")

    # 軸ラベルとタイトル
    ax.set_xlabel(cols[0])
    ax.set_ylabel(cols[1])
    ax.set_zlabel(cols[2])
    ax.set_title(f"{args.table} 3D plot (黒点)")

    ax.view_init(elev=25, azim=-60)
    plt.tight_layout()
    plt.savefig(args.out, dpi=150)
    plt.show()
    print(f"[INFO] 保存: {os.path.abspath(args.out)}")

if __name__ == "__main__":
    main()
