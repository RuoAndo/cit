import time, psutil
try:
    import wmi
except Exception:
    wmi = None

def get_cpu_load():
    return psutil.cpu_percent(interval=1)

def _query_lhm():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        temps = [(s.Name, s.Value) for s in c.Sensor() if getattr(s,"SensorType","")=="Temperature" and "cpu" in s.Name.lower()]
        if temps:
            # 代表値：最大
            name, val = max(temps, key=lambda x: x[1] if x[1] is not None else -999)
            return ("LibreHardwareMonitor", name, float(val))
    except: pass
    return None

def _query_ohm():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temps = [(s.Name, s.Value) for s in c.Sensor() if getattr(s,"SensorType","")=="Temperature" and "cpu" in s.Name.lower()]
        if temps:
            name, val = max(temps, key=lambda x: x[1] if x[1] is not None else -999)
            return ("OpenHardwareMonitor", name, float(val))
    except: pass
    return None

def _query_acpi():
    if wmi is None: return None
    try:
        c = wmi.WMI(namespace="root\\wmi")
        rows = c.MSAcpi_ThermalZoneTemperature()
        if rows:
            vals = [r.CurrentTemperature/10 - 273.15 for r in rows if hasattr(r,"CurrentTemperature")]
            if vals:
                return ("ACPI", "ThermalZone", float(max(vals)))
    except: pass
    return None

def get_cpu_temp():
    for f in (_query_lhm, _query_ohm, _query_acpi):
        res = f()
        if res is not None:
            src, name, v = res
            if -50 < v < 150:
                return res
    return None

print("CPU負荷率と温度を1秒ごとに取得します。Ctrl+Cで停止。")
print("※ 温度が取得不可の場合は、LHM/OHMを起動 or 管理者として実行を試してください。")

while True:
    try:
        load = get_cpu_load()          # ここで1秒待つ
        temp_info = get_cpu_temp()
        if temp_info is None:
            print(f"CPU使用率: {load:5.1f}% | 温度: 取得不可")
        else:
            src, name, t = temp_info
            print(f"CPU使用率: {load:5.1f}% | 温度: {t:5.1f}℃ ({src}:{name})")
    except KeyboardInterrupt:
        print("\n終了します。")
        break
    except Exception as e:
        print(f"エラー: {e}")
        time.sleep(1)
