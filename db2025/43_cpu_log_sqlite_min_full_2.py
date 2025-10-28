# cpu_log_sqlite_min_full.py
# 1秒ごとにCPU/メモリ等を観測し、標準出力へは全項目CSV、
# SQLiteへは (1)4列のcpu_metrics_min と (2)全項目のcpu_metrics_full を保存。
# 起動時に既存DBを安全に削除（ロック時は退避改名）。取得不能値はDBでNULL。

import json, os, socket, sqlite3, time, sys, csv, signal, atexit, math
from datetime import datetime, timezone
import psutil

# ===== 設定 =====
DB_PATH       = "cpu_metrics.db"
INTERVAL      = 1.0
BATCH_COMMIT  = 10
# ===============

# 標準出力はUTF-8/LFに統一（Windows対策）
try:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
except Exception:
    pass

# 既存DBを削除（ロック中なら退避改名）
if os.path.exists(DB_PATH):
    try:
        os.remove(DB_PATH)
        print(f"[INIT] removed: {DB_PATH}", file=sys.stderr)
    except PermissionError:
        base, ext = os.path.splitext(DB_PATH)
        bak = f"{base}-{int(time.time())}.bak{ext}"
        try:
            os.replace(DB_PATH, bak)
            print(f"[INIT] renamed locked DB -> {bak}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] backup failed: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] remove failed: {e}", file=sys.stderr)

# Windows 温度取得用（任意）
try:
    import wmi  # type: ignore
except Exception:
    wmi = None

HOSTNAME = socket.gethostname()
USERNAME = os.environ.get("USERNAME") or os.environ.get("USER")
STOP = False

def _stop(*_):
    global STOP
    STOP = True

# 安全停止
signal.signal(signal.SIGINT, _stop)
for sig in ("SIGTERM", "SIGBREAK"):
    if hasattr(signal, sig):
        try:
            signal.signal(getattr(signal, sig), _stop)
        except Exception:
            pass

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def _f(x):
    if x is None: return None
    try:
        xx = float(x)
        if math.isnan(xx) or math.isinf(xx):
            return None
        return xx
    except Exception:
        return None

def _i(x):
    if x is None: return None
    try:
        return int(x)
    except Exception:
        try:
            xx = float(x)
            if math.isnan(xx) or math.isinf(xx):
                return None
            return int(xx)
        except Exception:
            return None

def _json(v):
    # None/空配列/空辞書/JSON化失敗はNone（DBでNULL）
    if v is None: return None
    if isinstance(v, (list, dict)) and len(v) == 0: return None
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return None

def _num(x):
    if x is None: return None
    try:
        xx = float(x)
        if math.isnan(xx) or math.isinf(xx):
            return None
        return xx
    except Exception:
        return None

# --- CPU温度（取得できる範囲で） ---
def _wmi_values(ns: str, ok) -> list:
    try:
        c = wmi.WMI(namespace=ns)  # type: ignore
        return [s.Value for s in c.Sensor() if ok(s)]
    except Exception:
        return []

def get_cpu_temp_c():
    # 1) psutil
    try:
        temps = getattr(psutil, "sensors_temperatures", lambda: {})()
        for _, arr in temps.items():
            for t in arr:
                name = (getattr(t, "label", None) or getattr(t, "sensor", None) or "").lower()
                cur = getattr(t, "current", None)
                if cur is None: continue
                if ("cpu" in name or "package" in name) and -50 < cur < 150:
                    return _num(cur)
        for _, arr in temps.items():
            for t in arr:
                cur = getattr(t, "current", None)
                if cur is not None and -50 < cur < 150:
                    return _num(cur)
    except Exception:
        pass
    # 2) Windows: Libre/OpenHardwareMonitor / ACPI
    if wmi is not None:
        try:
            vals = _wmi_values("root\\LibreHardwareMonitor",
                               lambda s: getattr(s, "SensorType", "") == "Temperature" and "cpu" in (s.Name or "").lower())
            if not vals:
                vals = _wmi_values("root\\OpenHardwareMonitor",
                                   lambda s: getattr(s, "SensorType", "") == "Temperature" and "cpu" in (s.Name or "").lower())
            if vals:
                v = _num(max([v for v in vals if v is not None]))
                return v if (v is not None and -50 < v < 150) else None
        except Exception:
            pass
        try:
            c = wmi.WMI(namespace="root\\wmi")  # type: ignore
            rows = c.MSAcpi_ThermalZoneTemperature()
            if rows:
                cs = []
                for r in rows:
                    try:
                        cs.append(r.CurrentTemperature/10 - 273.15)
                    except Exception:
                        pass
                if cs:
                    v = _num(max(cs))
                    return v if (v is not None and -50 < v < 150) else None
        except Exception:
            pass
    return None

# --- DB スキーマ ---
DDL_MIN = """
CREATE TABLE IF NOT EXISTS cpu_metrics_min (
  ts               TEXT    NOT NULL,
  cpu_percent      REAL    NOT NULL,
  cpu_ctx_switches INTEGER,
  temp_c           REAL
);
CREATE INDEX IF NOT EXISTS idx_cpu_metrics_min_ts ON cpu_metrics_min(ts);
"""

DDL_FULL = """
CREATE TABLE IF NOT EXISTS cpu_metrics_full (
  ts               TEXT    NOT NULL,
  cpu_percent      REAL,
  temp_c           REAL,

  cpu_user_pct     REAL,
  cpu_system_pct   REAL,
  cpu_idle_pct     REAL,
  cpu_iowait_pct   REAL,

  cpu_ctx_switches INTEGER,
  cpu_interrupts   INTEGER,
  cpu_soft_intr    INTEGER,
  cpu_syscalls     INTEGER,

  cpu_logical      INTEGER,
  cpu_physical     INTEGER,

  cpu_freq_mhz       REAL,
  cpu_freq_min_mhz   REAL,
  cpu_freq_max_mhz   REAL,

  per_core_cpu     TEXT,   -- JSON
  per_core_freq    TEXT,   -- JSON

  mem_percent      REAL,
  mem_total        INTEGER,
  mem_available    INTEGER,
  mem_used         INTEGER,
  mem_free         INTEGER,
  mem_cached       INTEGER,
  mem_buffers      INTEGER,
  mem_shared       INTEGER,

  swap_percent     REAL,
  swap_total       INTEGER,
  swap_used        INTEGER,
  swap_free        INTEGER,
  swap_sin         INTEGER,
  swap_sout        INTEGER,

  load1            REAL,
  load5            REAL,
  load15           REAL,

  hostname         TEXT,
  username         TEXT
);
CREATE INDEX IF NOT EXISTS idx_cpu_metrics_full_ts ON cpu_metrics_full(ts);
"""

def open_db(path: str):
    con = sqlite3.connect(path, isolation_level="DEFERRED", timeout=10.0)
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    cur.execute("PRAGMA busy_timeout=5000;")
    cur.execute("PRAGMA temp_store=MEMORY;")
    cur.execute("PRAGMA mmap_size=134217728;")
    cur.executescript(DDL_MIN)
    cur.executescript(DDL_FULL)
    return con, cur

# 終了時クリーンアップ
_con = None
def _cleanup():
    global _con
    if _con is not None:
        try: _con.commit()
        except Exception: pass
        try: _con.close()
        except Exception: pass
atexit.register(_cleanup)

# CSVヘッダ（全項目）
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
        "cpu_percent": _f(cpu_total),
        "temp_c": _f(temp),

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
        "per_core_cpu": per_core_pct,
        "per_core_freq": per_core_freq,

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
    global _con
    con, cur = open_db(DB_PATH)
    _con = con

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(FIELD_ORDER)

    inserted = 0
    next_tick = time.perf_counter()  # 自前で1秒刻み管理

    try:
        while not STOP:
            # 次の刻みまで待機
            now = time.perf_counter()
            if now < next_tick:
                time.sleep(next_tick - now)
            next_tick += INTERVAL

            # 計測（待たない取得）
            cpu_total = psutil.cpu_percent(interval=None)
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

            per_core_pct  = psutil.cpu_percent(percpu=True, interval=None)
            try:
                per_core_freq = psutil.cpu_freq(percpu=True)
                per_core_freq = [x.current for x in per_core_freq] if per_core_freq else None
            except Exception:
                per_core_freq = None

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
                l1, l5, l15 = os.getloadavg()
            except Exception:
                l1 = l5 = l15 = None

            ts = now_iso()

            # --- DB: 4列ミニ（Noneは自動でNULL） ---
            try:
                cur.execute(
                    "INSERT INTO cpu_metrics_min (ts, cpu_percent, cpu_ctx_switches, temp_c) VALUES (?,?,?,?)",
                    (ts, _f(cpu_total), _i(ctx_sw), _f(temp))
                )
                inserted += 1
                if inserted % BATCH_COMMIT == 0:
                    con.commit()
            except Exception as e:
                print(f"[WARN] insert(min) failed at {ts}: {e}", file=sys.stderr)

            # --- DB: フル項目（per_coreはJSONへ。失敗/空はNULL） ---
            try:
                cur.execute("""
                    INSERT INTO cpu_metrics_full (
                      ts, cpu_percent, temp_c,
                      cpu_user_pct, cpu_system_pct, cpu_idle_pct, cpu_iowait_pct,
                      cpu_ctx_switches, cpu_interrupts, cpu_soft_intr, cpu_syscalls,
                      cpu_logical, cpu_physical,
                      cpu_freq_mhz, cpu_freq_min_mhz, cpu_freq_max_mhz,
                      per_core_cpu, per_core_freq,
                      mem_percent, mem_total, mem_available, mem_used, mem_free, mem_cached, mem_buffers, mem_shared,
                      swap_percent, swap_total, swap_used, swap_free, swap_sin, swap_sout,
                      load1, load5, load15,
                      hostname, username
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ts, _f(cpu_total), _f(temp),
                    _f(cpu_user), _f(cpu_sys), _f(cpu_idle), _f(cpu_iowait),
                    _i(ctx_sw), _i(intr), _i(softintr), _i(syscalls),
                    _i(logical), _i(physical),
                    _f(fcur), _f(fmn), _f(fmx),
                    _json(per_core_pct), _json(per_core_freq),
                    _f(mem_pct), _i(mem_total), _i(mem_avail), _i(mem_used), _i(mem_free), _i(mem_cached), _i(mem_buf), _i(mem_share),
                    _f(swap_pct), _i(swap_total), _i(swap_used), _i(swap_free), _i(swap_sin), _i(swap_sout),
                    _f(l1), _f(l5), _f(l15),
                    HOSTNAME, USERNAME
                ))
                if inserted % BATCH_COMMIT == 0:
                    con.commit()
            except Exception as e:
                print(f"[WARN] insert(full) failed at {ts}: {e}", file=sys.stderr)

            # --- CSV: 全項目を1行出力（Noneは空文字で可） ---
            rec = to_record_dict(
                ts, cpu_total, temp,
                cpu_user, cpu_sys, cpu_idle, cpu_iowait,
                ctx_sw, intr, softintr, syscalls,
                logical, physical,
                fcur, fmn, fmx,
                per_core_pct, per_core_freq,
                mem_pct, mem_total, mem_avail, mem_used, mem_free, mem_cached, mem_buf, mem_share,
                swap_pct, swap_total, swap_used, swap_free, swap_sin, swap_sout,
                l1, l5, l15
            )

            row = []
            for key in FIELD_ORDER:
                v = rec.get(key)
                if isinstance(v, (list, dict)):
                    row.append(json.dumps(v, ensure_ascii=False))
                elif v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
                    row.append("")
                else:
                    row.append(v)
            writer.writerow(row)
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        try: con.commit()
        except Exception: pass
        try: con.close()
        except Exception: pass

if __name__ == "__main__":
    main()
