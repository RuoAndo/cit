# cpu_load_temp_1s.py
# 1秒ごとにCPU使用率と温度を取得（Windows想定）
# 優先: LibreHardwareMonitor WMI → OpenHardwareMonitor WMI → ACPI ThermalZone → 温度なし

import time
import psutil

# WMIは遅延インポート（環境にない場合でも動くように）
try:
    import wmi
except Exception:
    wmi = None

def get_cpu_load():
    # interval=1 で直近1秒の平均を返す
    return psutil.cpu_percent(interval=1)

def _query_lhm_temperatures():
    """LibreHardwareMonitor の WMI からCPU温度群を取得（起動中のみ有効）"""
    if wmi is None:
        return []
    try:
        c = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        sensors = c.Sensor()  # すべて取得
        temps = [s.Value for s in sensors if getattr(s, "SensorType", "") == "Temperature" and "cpu" in s.Name.lower()]
        return temps
    except Exception:
        return []

def _query_ohm_temperatures():
    """OpenHardwareMonitor の WMI からCPU温度群を取得（起動中のみ有効）"""
    if wmi is None:
        return []
    try:
        c = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensors = c.Sensor()
        temps = [s.Value for s in sensors if getattr(s, "SensorType", "") == "Temperature" and "cpu" in s.Name.lower()]
        return temps
    except Exception:
        return []

def _query_acpi_temperature():
    """ACPI ThermalZone から温度を取得（0.1K → ℃）。大雑把、機種によっては0や固定値。"""
    if wmi is None:
        return None
    try:
        c = wmi.WMI(namespace="root\\wmi")
        rows = c.MSAcpi_ThermalZoneTemperature()
        if rows:
            # 複数ある場合は最大を代表値に
            cs = [r.CurrentTemperature / 10.0 - 273.15 for r in rows if hasattr(r, "CurrentTemperature")]
            if cs:
                return max(cs)
    except Exception:
        return None
    return None

def get_cpu_temperature_c():
    """
    温度取得（優先度順でトライ）
    1) LibreHardwareMonitor（推奨・要起動）
    2) OpenHardwareMonitor（要起動）
    3) ACPI ThermalZone（粗い/未対応PCあり）
    取得できなければ None
    """
    # 1) LibreHardwareMonitor
    temps = _query_lhm_temperatures()
    if temps:
        return max(temps)  # CPU Package などの最大を採用

    # 2) OpenHardwareMonitor
    temps = _query_ohm_temperatures()
    if temps:
        return max(temps)

    # 3) ACPI
    acpi = _query_acpi_temperature()
    if acpi is not None and acpi > -50 and acpi < 150:  # ざっくりフィルタ
        return acpi

    return None

def main():
    print("CPU負荷率と温度を1秒ごとに取得します。Ctrl+Cで停止。")
    print("※ 温度が None の場合は、管理者で実行 or LibreHardwareMonitor を起動して再実行してください。")
    while True:
        try:
            load = get_cpu_load()          # ここで1秒待つ
            temp = get_cpu_temperature_c() # 温度取得はできたら即返る

            if temp is None:
                print(f"CPU使用率: {load:5.1f}% | 温度: 取得不可")
            else:
                print(f"CPU使用率: {load:5.1f}% | 温度: {temp:5.1f}℃")
        except KeyboardInterrupt:
            print("\n終了します。")
            break
        except Exception as e:
            print(f"エラー: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
