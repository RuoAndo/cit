# cpu_log_sqlite.py
# 1秒ごとに CPU使用率 と 温度 を取得して SQLite3 に保存
#   テーブル: cpu_metrics(ts TEXT ISO8601, cpu_percent REAL, temp_c REAL NULL)
# 使い方:
#   pip install psutil wmi   # wmiはWindowsで温度取得に使用（任意）
#   python cpu_log_sqlite.py --db cpu_metrics.db --interval 1

import time
import sqlite3
import argparse
import psutil
from datetime import datetime, timezone

# wmiは任意（温度取得のため）。無ければ温度はNULLになる可能性あり
try:
    import wmi
except Exception:
    wmi = None

def now_iso():
    # UTCのISO8601（SQLiteの時系列処理が安定）
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# ---- 温度取得まわり（LHM→OHM→ACPIの順にトライ） ----
def _query_lhm():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        temps = [(s.Name, s.Value) for s in c.Sensor()
                 if getattr(s, "SensorType", "") == "Temperature" and "cpu" in s.Name.lower()]
        if temps:
            # 代表として最大値
            return float(max(v for _, v in temps if v is not None))
    except Exception:
        pass
    return None

def _query_ohm():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temps = [(s.Name, s.Value) for s in c.Sensor()
                 if getattr(s, "SensorType", "") == "Temperature" and "cpu" in s.Name.lower()]
        if temps:
            return float(max(v for _, v in temps if v is not None))
    except Exception:
        pass
    return None

def _query_acpi():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\wmi")
        rows = c.MSAcpi_ThermalZoneTemperature()
        if rows:
            vs = [r.CurrentTemperature/10 - 273.15
                  for r in rows if hasattr(r, "CurrentTemperature")]
            if vs:
                return float(max(vs))
    except Exception:
        pass
    return None

def get_temp_c():
    for fn in (_query_lhm, _query_ohm, _query_acpi):
        v = fn()
        if v is not None and -50 < v < 150:
            return v
    return None

# ---- SQLite 準備 ----
DDL = """
CREATE TABLE IF NOT EXISTS cpu_metrics (
  ts          TEXT    NOT NULL,   -- ISO8601 (UTC)
  cpu_percent REAL    NOT NULL,   -- 0.0 - 100.0
  temp_c      REAL                -- 取得不可ならNULL
);
CREATE INDEX IF NOT EXISTS idx_cpu_metrics_ts ON cpu_metrics(ts);
"""

def open_db(path):
    con = sqlite3.connect(path, isolation_level=None)  # autocommit
    cur = con.cursor()
    # 軽量・耐障害性のバランス
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    # DDL
    cur.executescript(DDL)
    return con, cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="cpu_metrics.db", help="SQLite DBファイルパス")
    ap.add_argument("--interval", type=float, default=1.0, help="取得間隔(秒)")
    ap.add_argument("--batch", type=int, default=10, help="この件数ごとにcommit（WALでも安全側）")
    args = ap.parse_args()

    con, cur = open_db(args.db)

    print(f"開始: {args.db} に 1秒ごと記録（Ctrl+Cで終了）")
    print("温度がNoneになる場合は、管理者実行や LibreHardwareMonitor/OpenHardwareMonitor の併用を検討。")

    inserted = 0
    try:
        while True:
            # psutilはintervalで直近区間の平均を返す → ここで実質 args.interval 待機
            cpu = psutil.cpu_percent(interval=args.interval)
            temp = get_temp_c()  # 取得できなければ None

            ts = now_iso()
            cur.execute("INSERT INTO cpu_metrics(ts, cpu_percent, temp_c) VALUES (?, ?, ?)",
                        (ts, float(cpu), None if temp is None else float(temp)))
            inserted += 1

            # 進行表示（必要なければ消してOK）
            if temp is None:
                print(f"{ts} | CPU: {cpu:5.1f}% | Temp: None")
            else:
                print(f"{ts} | CPU: {cpu:5.1f}% | Temp: {temp:5.1f}°C")

            # 明示commit（WALでも念のためバッチング）
            if inserted % args.batch == 0:
                con.commit()

    except KeyboardInterrupt:
        print("\n停止要求を受けました。フラッシュ中…")
    finally:
        try:
            con.commit()
        except Exception:
            pass
        con.close()
        print(f"終了。挿入件数: {inserted}")

if __name__ == "__main__":
    main()

