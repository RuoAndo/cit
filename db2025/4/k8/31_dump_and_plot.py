# 31_dump_and_plot.py
# EXCLUDE_COLS 以外の列からランダムに3列選び、
# その3列がすべて非NULLの行を全件プロットする（見つかるまで試行）

import sqlite3, random
import matplotlib.pyplot as plt
from itertools import combinations
from collections import defaultdict

DB_PATH = "cpu_metrics.db"
TABLE   = "cpu_metrics"
SEED    = None     # 例: 42 で固定。None で毎回ランダム
MAX_TRIES = 300    # 組合せを最大いくつ試すか（候補が多いと全探索）

EXCLUDE_COLS = {
    "ts", "per_core_cpu", "per_core_freq", "hostname", "username",
    "cpu_logical", "cpu_physical", "mem_total", "swap_total",
    "cpu_freq_min_mhz", "cpu_freq_max_mhz"
}

def get_all_columns(db_path, table):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute(f"PRAGMA table_info({table});")
    cols = [row[1] for row in cur.fetchall()]  # name=row[1]
    con.close()
    return cols

def nonnull_counts(db_path, table, cols):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()
    counts = {}
    for c in cols:
        cur.execute(f"SELECT COUNT({c}) FROM {table} WHERE {c} IS NOT NULL;")
        counts[c] = cur.fetchone()[0]
    con.close()
    return counts

def has_rows_for_triplet(db_path, table, triplet):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()
    where = " AND ".join([f"{c} IS NOT NULL" for c in triplet])
    cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {where};")
    cnt = cur.fetchone()[0]
    con.close()
    return cnt > 0

def fetch_all_triplet(db_path, table, triplet):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()
    where = " AND ".join([f"{c} IS NOT NULL" for c in triplet])
    cur.execute(f"SELECT {', '.join(triplet)} FROM {table} WHERE {where} ORDER BY ts;")
    rows = cur.fetchall()
    con.close()
    return rows

def main():
    if SEED is not None:
        random.seed(SEED)

    all_cols = get_all_columns(DB_PATH, TABLE)
    candidates = [c for c in all_cols if c not in EXCLUDE_COLS]
    if len(candidates) < 3:
        raise SystemExit("候補列が3つ未満です。EXCLUDE_COLSやスキーマを確認してください。")

    # 非NULL件数が多い列を優先的に試すため、まず件数を取る
    nnc = nonnull_counts(DB_PATH, TABLE, candidates)
    # 非NULLが0の列は最初から除外
    candidates = [c for c in candidates if nnc.get(c, 0) > 0]
    if len(candidates) < 3:
        print("非NULLが存在する列が3未満です。各列の非NULL件数：")
        for k in sorted(nnc, key=nnc.get, reverse=True):
            print(f"  {k}: {nnc[k]}")
        raise SystemExit("有効な組合せがありません。")

    # 非NULL件数の多い列ほど先に試す（シャッフルして偏りを軽く）
    random.shuffle(candidates)
    candidates.sort(key=lambda c: nnc[c], reverse=True)

    tried = 0
    chosen = None

    # 優先順で全組合せを作り、先頭から最大MAX_TRIESまで試す
    triplets = list(combinations(candidates, 3))
    # 組合せが多すぎる場合はランダムサンプル
    if len(triplets) > MAX_TRIES:
        triplets = random.sample(triplets, MAX_TRIES)

    for trip in triplets:
        tried += 1
        if has_rows_for_triplet(DB_PATH, TABLE, trip):
            chosen = trip
            break

    if not chosen:
        print(f"有効な3列の組合せが見つかりませんでした（試行数 {tried}）。各列の非NULL件数：")
        for k in sorted(nnc, key=nnc.get, reverse=True):
            print(f"  {k}: {nnc[k]}")
        raise SystemExit("別のデータ期間やEXCLUDE_COLSを調整してください。")

    # データ取得
    rows = fetch_all_triplet(DB_PATH, TABLE, chosen)
    xs, ys, zs = [], [], []
    dropped = 0
    for r in rows:
        try:
            xs.append(float(r[0]))
            ys.append(float(r[1]))
            zs.append(float(r[2]))
        except Exception:
            dropped += 1

    if not xs:
        raise SystemExit(f"選ばれた列に数値化できるデータがありません: {chosen}")

    print(f"Chosen columns: {chosen[0]}, {chosen[1]}, {chosen[2]} "
          f"(rows: {len(xs)}, dropped: {dropped}, tried: {tried})")

    # 3D散布図
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs)  # デフォルト色
    ax.set_xlabel(chosen[0]); ax.set_ylabel(chosen[1]); ax.set_zlabel(chosen[2])
    ax.set_title("3D Scatter (all rows)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
