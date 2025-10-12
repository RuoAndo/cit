import sys
try:
    import wmi
except Exception:
    print("wmiモジュール未導入: pip install wmi")
    sys.exit(1)

def try_ns(ns):
    try:
        c = wmi.WMI(namespace=ns)
        sensors = c.Sensor()
        temps = [(s.Name, getattr(s, "Value", None)) for s in sensors if getattr(s, "SensorType","")=="Temperature"]
        return temps
    except Exception as e:
        return f"NG: {e}"

for ns in ["root\\LibreHardwareMonitor", "root\\OpenHardwareMonitor"]:
    print(f"[{ns}] ->", try_ns(ns))

# ACPI（粗い）
try:
    c = wmi.WMI(namespace="root\\wmi")
    rows = c.MSAcpi_ThermalZoneTemperature()
    cs = [r.CurrentTemperature/10 - 273.15 for r in rows] if rows else []
    print("[root\\wmi MSAcpi_ThermalZoneTemperature] ->", cs)
except Exception as e:
    print("[root\\wmi] -> NG:", e)
