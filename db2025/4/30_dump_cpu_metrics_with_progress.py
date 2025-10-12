# dump_cpu_metrics_stream.py
# cpu_metrics を CSV で 1行ずつ出力（ヘッダ→各行を逐次フラッシュ）
# 使い方: python dump_cpu_metrics_stream.py  （必要なら下部の定数を調整）

import csv
import sqlite3
import sys

# ===== 設定 =====
DB_PATH   = "cpu_metrics.db"                          # 対象DB
OUT_CSV   = None      # None=標準出力, それ以外=ファイル名
START_ISO = None      # 例: "2025-10-12T00:00:00.000000Z"
END_ISO   = None      # 例: "2025-10-12T23:59:59.999999Z"
ORDER_BY  = "ts"      # 並び順キー
# ===============

def build_query():
    sql = "SELECT * FROM cpu_metrics"
    params = []
    conds = []
    if START_ISO:
        conds.append("ts >= ?"); params.append(START_ISO)
    if END_ISO:
        conds.append("ts <= ?"); params.append(END_ISO)
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += f" ORDER BY {ORDER_BY}"
    return sql, params

def main():
    # 読み取り専用接続（他プロセスが書き込み中でも安全側）
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = con.cursor()

    sel_sql, sel_params = build_query()
    cur.execute(sel_sql, sel_params)

    # 出力先
    close_needed = False
    if OUT_CSV:
        f = open(OUT_CSV, "w", newline="", encoding="utf-8")
        close_needed = True
    else:
        f = sys.stdout
        # 行バッファリング（Python 3.7+）
        try:
            f.reconfigure(line_buffering=True)
        except Exception:
            pass

    writer = csv.writer(f, lineterminator="\n")

    # ヘッダ（カラム名）出力
    header = [d[0] for d in cur.description]
    writer.writerow(header)
    if OUT_CSV is None:
        f.flush()

    # 1行ずつ書き出し（逐次フラッシュ）
    row = cur.fetchone()
    while row is not None:
        writer.writerow(row)
        if OUT_CSV is None:
            f.flush()
        row = cur.fetchone()

    if close_needed:
        f.close()
    con.close()

if __name__ == "__main__":
    main()
