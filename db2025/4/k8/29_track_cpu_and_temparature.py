# cpu_log_sqlite.py (header+values CSV)
# 1秒ごとにCPU/メモリ系メトリクスをSQLite3へ保存しつつ、
# 標準出力には「1行目=項目名、以降=値のみ」をCSVで出力します。
# 引数は使わずハードコーディング。

import json, os, socket, sqlite3, time, sys, csv
from datetime import datetime, timezone
import psutil

# ===== 設定 =====
DB_PATH   = "cpu_metrics.db"
INTERVAL  = 1.0
BATCH_COMMIT = 10
# ===============

try:
    import wmi  # type: ignore
except Exception:
    wmi = None

HOSTNAME = socket.gethostname()
USERNAME = os.environ.get("USERNAME") or os.environ.get("USER")

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def _wmi_values(ns: str, ok) -> list:
    try:
        c = wmi.WMI(namespace=ns)  # type: ignore
        return [s.Value for s in c.Sensor() if ok(s)]
    except Exception:
        return []

def get_cpu_temp_c():
    if wmi is not None:
        vals = _wmi_values("root\\LibreHardwareMonitor",
                           lambda s: getattr(s, "SensorType", "") == "Temperature" and "cpu" in (s.Name or "").lower())
        if not vals:
            vals = _wmi_values("root\\OpenHardwareMonitor",
                               lambda s: getattr(s, "SensorType", "") == "Temperature" and "cpu" in (s.Name or "").lower())
        if vals:
            v = max([v for v in vals if v is not None])
            return v if -50 < v < 150 else None
    try:
        if wmi is None:
            return None
        c = wmi.WMI(namespace="root\\wmi")  # type: ignore
        rows = c.MSAcpi_ThermalZoneTemperature()
        if rows:
            cs = [r.CurrentTemperature/10 - 273.15 for r in rows if hasattr(r, "CurrentTemperature")]
            if cs:
                v = max(cs)
                return v if -50 < v < 150 else None
    except Exception:
        pass
    return None

DDL_BASE = """
CREATE TABLE IF NOT EXISTS cpu_metrics (
  ts          TEXT    NOT NULL,
  cpu_percent REAL    NOT NULL,
  temp_c      REAL
);
CREATE INDEX IF NOT EXISTS idx_cpu_metrics_ts ON cpu_metrics(ts);
"""

EXTRA_COLS = [
    ("cpu_user_pct",     "REAL"),
    ("cpu_system_pct",   "REAL"),
    ("cpu_idle_pct",     "REAL"),
    ("cpu_iowait_pct",   "REAL"),
    ("cpu_ctx_switches", "INTEGER"),
    ("cpu_interrupts",   "INTEGER"),
    ("cpu_soft_intr",    "INTEGER"),
    ("cpu_syscalls",     "INTEGER"),
    ("cpu_logical",      "INTEGER"),
    ("cpu_physical",     "INTEGER"),
    ("cpu_freq_mhz",     "REAL"),
    ("cpu_freq_min_mhz", "REAL"),
    ("cpu_freq_max_mhz", "REAL"),
    ("per_core_cpu",     "TEXT"),
    ("per_core_freq",    "TEXT"),
    ("mem_percent",      "REAL"),
    ("mem_total",        "INTEGER"),
    ("mem_available",    "INTEGER"),
    ("mem_used",         "INTEGER"),
    ("mem_free",         "INTEGER"),
    ("mem_cached",       "INTEGER"),
    ("mem_buffers",      "INTEGER"),
    ("mem_shared",       "INTEGER"),
    ("swap_percent",     "REAL"),
    ("swap_total",       "INTEGER"),
    ("swap_used",        "INTEGER"),
    ("swap_free",        "INTEGER"),
    ("swap_sin",         "INTEGER"),
    ("swap_sout",        "INTEGER"),
    ("load1",            "REAL"),
    ("load5",            "REAL"),
    ("load15",           "REAL"),
    ("hostname",         "TEXT"),
    ("username",         "TEXT"),
]

def _existing_cols(cur, table="cpu_metrics"):
    cur.execute(f"PRAGMA table_info({table});")
    return {row[1] for row in cur.fetchall()}

def open_db(path: str):
    con = sqlite3.connect(path, isolation_level=None, timeout=10.0)
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    cur.executescript(DDL_BASE)
    have = _existing_cols(cur, "cpu_metrics")
    for name, typ in EXTRA_COLS:
        if name not in have:
            cur.execute(f"ALTER TABLE cpu_metrics ADD COLUMN {name} {typ};")
    return con, cur

def _f(x): return None if x is None else float(x)
def _i(x): return None if x is None else int(x)

# ヘッダ順（出力＆CSV列順）
FIELD_ORDER = [
    "ts","cpu_percent","temp_c",
    "cpu_user_pct","cpu_system_pct","cpu_idle_pct","cpu_iowait_pct",
    "cpu_ctx_switches","cpu_interrupts","cpu_soft_intr","cpu_syscalls",
    "cpu_logical","cpu_physical",
    "cpu_freq_mhz","cpu_freq_min_mhz","cpu_freq_max_mhz",
    "per_core_cpu","per_core_freq",
    "mem_percent","mem_total","mem_available","mem_used","mem_free","mem_cached","mem_buffers","mem_shared",
    "swap_percent","swap_total","swap_used","swap_free","swap_sin","swap_sout",
    "load1","load5","load15",
    "hostname","username",
]

def to_record_dict(ts, cpu_total, temp,
                   cpu_user, cpu_sys, cpu_idle, cpu_iowait,
                   ctx_sw, intr, softintr, syscalls,
                   logical, physical,
                   fcur, fmn, fmx,
                   per_core_pct, per_core_freq,
                   mem_pct, mem_total, mem_avail, mem_used, mem_free, mem_cached, mem_buf, mem_share,
                   swap_pct, swap_total, swap_used, swap_free, swap_sin, swap_sout,
                   l1, l5, l15):
    return {
        "ts": ts,
        "cpu_percent": float(cpu_total),
        "temp_c": None if temp is None else float(temp),

        "cpu_user_pct": _f(cpu_user),
        "cpu_system_pct": _f(cpu_sys),
        "cpu_idle_pct": _f(cpu_idle),
        "cpu_iowait_pct": _f(cpu_iowait),
        "cpu_ctx_switches": _i(ctx_sw),
        "cpu_interrupts": _i(intr),
        "cpu_soft_intr": _i(softintr),
        "cpu_syscalls": _i(syscalls),
        "cpu_logical": _i(logical),
        "cpu_physical": _i(physical),

        "cpu_freq_mhz": _f(fcur),
        "cpu_freq_min_mhz": _f(fmn),
        "cpu_freq_max_mhz": _f(fmx),
        "per_core_cpu": per_core_pct,                         # list
        "per_core_freq": per_core_freq,                       # list or None

        "mem_percent": _f(mem_pct),
        "mem_total": _i(mem_total),
        "mem_available": _i(mem_avail),
        "mem_used": _i(mem_used),
        "mem_free": _i(mem_free),
        "mem_cached": _i(mem_cached),
        "mem_buffers": _i(mem_buf),
        "mem_shared": _i(mem_share),

        "swap_percent": _f(swap_pct),
        "swap_total": _i(swap_total),
        "swap_used": _i(swap_used),
        "swap_free": _i(swap_free),
        "swap_sin": _i(swap_sin),
        "swap_sout": _i(swap_sout),

        "load1": _f(l1),
        "load5": _f(l5),
        "load15": _f(l15),

        "hostname": HOSTNAME,
        "username": USERNAME,
    }

def main():
    con, cur = open_db(DB_PATH)

    # CSVライター（Excel互換のダブルクォートで自動エスケープ）
    writer = csv.writer(sys.stdout, lineterminator="\n")

    # ヘッダ（項目名）を最初に1回だけ出力
    writer.writerow(FIELD_ORDER)

    inserted = 0
    try:
        while True:
            cpu_total = psutil.cpu_percent(interval=INTERVAL)
            temp = get_cpu_temp_c()

            ct = psutil.cpu_times_percent(interval=0.0)
            cpu_user   = getattr(ct, "user",   None)
            cpu_sys    = getattr(ct, "system", None)
            cpu_idle   = getattr(ct, "idle",   None)
            cpu_iowait = getattr(ct, "iowait", None)

            cs = psutil.cpu_stats()
            ctx_sw   = getattr(cs, "ctx_switches",    None)
            intr     = getattr(cs, "interrupts",      None)
            softintr = getattr(cs, "soft_interrupts", None)
            syscalls = getattr(cs, "syscalls",        None)

            logical  = psutil.cpu_count(logical=True)
            physical = psutil.cpu_count(logical=False)

            f   = psutil.cpu_freq()
            fmn = f.min if f else None
            fmx = f.max if f else None
            fcur= f.current if f else None

            per_core_pct  = psutil.cpu_percent(percpu=True, interval=0.0)
            per_core_freq = psutil.cpu_freq(percpu=True)
            per_core_freq = [x.current for x in per_core_freq] if per_core_freq else None

            vm = psutil.virtual_memory()
            mem_pct   = vm.percent
            mem_total = vm.total
            mem_avail = vm.available
            mem_used  = vm.used
            mem_free  = vm.free
            mem_cached= getattr(vm, "cached",  None)
            mem_buf   = getattr(vm, "buffers", None)
            mem_share = getattr(vm, "shared",  None)

            sw = psutil.swap_memory()
            swap_pct  = sw.percent
            swap_total= sw.total
            swap_used = sw.used
            swap_free = sw.free
            swap_sin  = getattr(sw, "sin",  None)
            swap_sout = getattr(sw, "sout", None)

            try:
                import os
                l1, l5, l15 = os.getloadavg()
            except Exception:
                l1 = l5 = l15 = None

            ts = now_iso()

            # DB書き込み
            cur.execute(
                """INSERT INTO cpu_metrics
                (ts,cpu_percent,temp_c,
                 cpu_user_pct,cpu_system_pct,cpu_idle_pct,cpu_iowait_pct,
                 cpu_ctx_switches,cpu_interrupts,cpu_soft_intr,cpu_syscalls,
                 cpu_logical,cpu_physical,
                 cpu_freq_mhz,cpu_freq_min_mhz,cpu_freq_max_mhz,
                 per_core_cpu,per_core_freq,
                 mem_percent,mem_total,mem_available,mem_used,mem_free,mem_cached,mem_buffers,mem_shared,
                 swap_percent,swap_total,swap_used,swap_free,swap_sin,swap_sout,
                 load1,load5,load15,hostname,username)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (ts, float(cpu_total), None if temp is None else float(temp),
                 _f(cpu_user), _f(cpu_sys), _f(cpu_idle), _f(cpu_iowait),
                 _i(ctx_sw), _i(intr), _i(softintr), _i(syscalls),
                 _i(logical), _i(physical),
                 _f(fcur), _f(fmn), _f(fmx),
                 json.dumps(per_core_pct, ensure_ascii=False),
                 json.dumps(per_core_freq, ensure_ascii=False) if per_core_freq is not None else None,
                 _f(mem_pct), _i(mem_total), _i(mem_avail), _i(mem_used), _i(mem_free),
                 _i(mem_cached), _i(mem_buf), _i(mem_share),
                 _f(swap_pct), _i(swap_total), _i(swap_used), _i(swap_free), _i(swap_sin), _i(swap_sout),
                 _f(l1), _f(l5), _f(l15), HOSTNAME, USERNAME)
            )
            inserted += 1
            if inserted % BATCH_COMMIT == 0:
                con.commit()

            # レコード辞書 → 値配列（配列はJSON文字列、Noneは空セル）
            rec = to_record_dict(ts, cpu_total, temp,
                                 cpu_user, cpu_sys, cpu_idle, cpu_iowait,
                                 ctx_sw, intr, softintr, syscalls,
                                 logical, physical,
                                 fcur, fmn, fmx,
                                 per_core_pct, per_core_freq,
                                 mem_pct, mem_total, mem_avail, mem_used, mem_free, mem_cached, mem_buf, mem_share,
                                 swap_pct, swap_total, swap_used, swap_free, swap_sin, swap_sout,
                                 l1, l5, l15)

            row = []
            for key in FIELD_ORDER:
                v = rec.get(key)
                if isinstance(v, (list, dict)):
                    row.append(json.dumps(v, ensure_ascii=False))
                elif v is None:
                    row.append("")
                else:
                    row.append(v)
            writer.writerow(row)
            # フラッシュ（ログ用途で即時出力したい場合）
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        try:
            con.commit()
        except Exception:
            pass
        con.close()

if __name__ == "__main__":
    main()
