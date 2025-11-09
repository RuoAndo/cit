#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3D plot from cpu_metrics_full by selecting any 3 items from 8 candidates.
- Always prints progress logs (hardcoded verbose)
- All errors are in English
- Smart NOT NULL filters: only applied when column actually has non-NULL rows
- Auto-fallback: if a chosen axis has zero usable values, it falls back to time_index
"""

import argparse
import sqlite3
import json
import math
import sys
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

MAP_NUM_TO_FIELD = {
    1: "time_index",     # generated
    2: "cpu_percent",
    3: "mem_percent",
    4: "temp_c",
    5: "cpu_percent",    # optionally filter >= 80
    6: "cpu_iowait_pct",
    7: "cpu_percent",
    8: "core0_usage",    # from per_core_cpu[0] JSON
}

CHOICES_DESC = {
    1: "time_index",
    2: "cpu_percent",
    3: "mem_percent",
    4: "temp_c",
    5: "cpu_percent (>=80% filterable)",
    6: "cpu_iowait_pct",
    7: "cpu_percent",
    8: "core0_usage (per_core_cpu[0])",
}

def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)

def _to_float_or_none(x):
    try:
        return None if x is None else float(x)
    except Exception:
        return None

def isnan(v):
    try:
        return math.isnan(v)
    except Exception:
        return False

def picks_to_required_columns(picks):
    cols = set()
    for n in picks:
        f = MAP_NUM_TO_FIELD[n]
        if f == "time_index":
            continue
        if f == "core0_usage":
            cols.add("per_core_cpu")   # JSON presence; content validated in Python
        else:
            cols.add(f)                # scalar column
    return cols

# ---------- DB helpers ----------
def connect(db_path):
    log(f"Connecting to database: {db_path}")
    try:
        return sqlite3.connect(db_path)
    except Exception as e:
        raise SystemExit(f"ERROR: Failed to connect to database: {e}")

def column_nonnull_count(con, table, col) -> int:
    q = f"SELECT COUNT(1) FROM {table} WHERE {col} IS NOT NULL"
    try:
        cur = con.cursor()
        return int(cur.execute(q).fetchone()[0])
    except Exception as e:
        raise SystemExit(f"ERROR: Failed to check non-NULL count for column '{col}': {e}")

def build_query(table, picks, order_desc=False, limit=None, con=None):
    base_cols = [
        "ts",
        "cpu_percent",
        "temp_c",
        "cpu_iowait_pct",
        "mem_percent",
        "per_core_cpu",
        "hostname",
    ]
    order = "DESC" if order_desc else "ASC"

    req = picks_to_required_columns(picks)
    not_null_terms, relaxed, applied = [], [], []

    if con is None:
        raise SystemExit("ERROR: Internal: connection is None in build_query.")

    for col in req:
        if col == "per_core_cpu":
            # JSON列はSQLではフィルタしない（Python側で検証）
            continue
        cnt = column_nonnull_count(con, table, col)
        if cnt > 0:
            applied.append(col)
            not_null_terms.append(f"{col} IS NOT NULL")
        else:
            relaxed.append(col)

    if applied:
        log(f"NOT NULL filters applied: {', '.join(applied)}")
    if relaxed:
        log(f"NOT NULL filters RELAXED (no non-NULL rows): {', '.join(relaxed)}")

    where_clause = ""
    if not_null_terms:
        where_clause = " WHERE " + " AND ".join(not_null_terms)

    sql = f"SELECT {', '.join(base_cols)} FROM {table}{where_clause} ORDER BY ts {order}"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return sql

def load_rows(db_path, table, picks, order_desc=False, limit=None):
    con = connect(db_path)
    log(f"Building query on table '{table}'...")
    sql = build_query(table, picks, order_desc=order_desc, limit=limit, con=con)
    log(f"SQL: {sql}")
    try:
        cur = con.cursor()
        rows = cur.execute(sql).fetchall()
    except Exception as e:
        con.close()
        raise SystemExit(f"ERROR: Failed to execute query: {e}")
    finally:
        con.close()
    log(f"Rows fetched: {len(rows)}")
    return rows

def parse_rows(rows):
    data = []
    n = len(rows)
    log("Parsing rows...")
    for i, row in enumerate(rows):
        ts, cpu_percent, temp_c, cpu_iowait_pct, mem_percent, per_core_cpu, hostname = row

        core0 = None
        if per_core_cpu:
            try:
                arr = json.loads(per_core_cpu)
                if isinstance(arr, list) and arr and arr[0] is not None:
                    core0 = float(arr[0])
            except Exception:
                pass

        data.append({
            "idx": i,
            "ts": ts,
            "cpu_percent": _to_float_or_none(cpu_percent),
            "temp_c": _to_float_or_none(temp_c),
            "cpu_iowait_pct": _to_float_or_none(cpu_iowait_pct),
            "mem_percent": _to_float_or_none(mem_percent),
            "core0_usage": core0,
            "hostname": hostname,
        })

        if n > 0 and i % max(1, n // 20) == 0:
            pct = (i + 1) * 100.0 / n
            log(f"Parsing progress: {pct:.1f}% ({i+1}/{n})")

    log("Parsing complete.")
    return data

# ---------- Axis & plot ----------
def pick_axis(series_num, data, apply_filters=False):
    field = MAP_NUM_TO_FIELD[series_num]
    if field == "time_index":
        return [i + 1 for i, _ in enumerate(data)]
    vals = []
    for row in data:
        val = row.get(field)
        if series_num == 5 and apply_filters:
            if val is not None and val < 80.0:
                val = None
        vals.append(val)
    return vals

def count_nonnull(arr):
    return sum(1 for v in arr if (v is not None and not isnan(v)))

def align_and_drop_na(x, y, z):
    X, Y, Z = [], [], []
    dropped = 0
    for a, b, c in zip(x, y, z):
        if a is None or b is None or c is None or any(map(isnan, (a, b, c))):
            dropped += 1
            continue
        X.append(a); Y.append(b); Z.append(c)
    log(f"Aligned points: {len(X)}; Dropped due to NA/NaN: {dropped}")
    return X, Y, Z

def fallback_axis_if_empty(axis_vals, label, axis_name, data):
    if count_nonnull(axis_vals) == 0:
        log(f"WARNING: Axis {axis_name} ('{label}') has no non-NULL values. Falling back to time_index.")
        return [i + 1 for i, _ in enumerate(data)], "time_index (fallback)"
    return axis_vals, label

def main():
    ap = argparse.ArgumentParser(description="3D plot from cpu_metrics_full by picking 3 items.")
    ap.add_argument("--db", required=True, help="SQLite DB file path (e.g., metrics.db)")
    ap.add_argument("--table", default="cpu_metrics_full", help="Table name (default: cpu_metrics_full)")
    ap.add_argument("--pick", default="4,5,8", help="Pick 3 numbers from 1-8, comma-separated (default: 4,5,8)")
    ap.add_argument("--limit", type=int, default=None, help="Limit rows (e.g., 5000)")
    ap.add_argument("--desc", action="store_true", help="Order by ts DESC (default ASC)")
    ap.add_argument("--apply-filters", action="store_true", help="Apply filters for choice 5 (cpu_percent >= 80)")
    args = ap.parse_args()

    log("=== Configuration Summary ===")
    log(f"DB: {args.db}")
    log(f"Table: {args.table}")
    log(f"Pick: {args.pick}")
    log(f"Limit: {args.limit}")
    log(f"Order: {'DESC' if args.desc else 'ASC'}")
    log(f"Apply filters (for choice 5): {args.apply_filters}")
    log("=============================")

    try:
        picks = [int(s.strip()) for s in args.pick.split(",")]
    except Exception:
        raise SystemExit("ERROR: --pick must be three integers (1-8), comma-separated. Example: --pick 4,5,8")
    if len(picks) != 3 or any(n < 1 or n > 8 for n in picks):
        raise SystemExit("ERROR: --pick must contain exactly three numbers in the range 1..8.")

    rows = load_rows(args.db, args.table, picks, order_desc=args.desc, limit=args.limit)
    if not rows:
        raise SystemExit("ERROR: No rows returned after applying optional NOT NULL filters. "
                         "Your dataset may not contain any non-NULL values for the chosen axes. "
                         "Try a different --pick (e.g., 1,2,8 or 1,3,6).")

    data = parse_rows(rows)

    log("Building axes from selections...")
    x = pick_axis(picks[0], data, apply_filters=args.apply_filters)
    y = pick_axis(picks[1], data, apply_filters=args.apply_filters)
    z = pick_axis(picks[2], data, apply_filters=args.apply_filters)

    xlabel = CHOICES_DESC[picks[0]]
    ylabel = CHOICES_DESC[picks[1]]
    zlabel = CHOICES_DESC[picks[2]]

    # Auto-fallback to time_index for any axis with zero non-NULL values
    x, xlabel = fallback_axis_if_empty(x, xlabel, "X", data)
    y, ylabel = fallback_axis_if_empty(y, ylabel, "Y", data)
    z, zlabel = fallback_axis_if_empty(z, zlabel, "Z", data)

    log(f"Non-null counts -> X:{count_nonnull(x)} Y:{count_nonnull(y)} Z:{count_nonnull(z)}")

    X, Y, Z = align_and_drop_na(x, y, z)
    if len(X) == 0:
        raise SystemExit("ERROR: No valid points to plot after filtering/NA removal. Adjust --pick or filters.")

    log("Rendering 3D scatter plot...")
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(X, Y, Z)  # default style
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(f"3D Plot: {xlabel}, {ylabel}, {zlabel}")
    log("Showing plot window.")
    plt.show()
    log("Done.")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if str(e):
            print(str(e), file=sys.stderr)
        sys.exit(e.code if isinstance(e.code, int) else 1)
    except Exception as e:
        print(f"ERROR: Unexpected failure: {e}", file=sys.stderr)
        sys.exit(1)
