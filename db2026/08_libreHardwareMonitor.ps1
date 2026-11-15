# ============================================================
# 07_libreHardwareMonitor.ps1
#
# LibreHardwareMonitor HTTP API
# CPU / HDD / SSD Temperature and CPU Load Monitor
#
# Windows PowerShell 5.1 / PowerShell 7
#
# Features:
#   - CPU temperature monitoring
#   - CPU load monitoring
#   - HDD / SSD temperature monitoring
#   - CSV logging
#   - Automatic sensor discovery
#   - Continue when CPU temperature is unavailable
#   - API reconnection
#   - Sensor list display
#
# Stop: Ctrl+C
# ============================================================

param(
    [string]$Url = "http://127.0.0.1:8085/data.json",
    [int]$IntervalSeconds = 1,
    [switch]$ShowAllSensors
)

$ErrorActionPreference = "Stop"

# ============================================================
# 1. Initial settings
# ============================================================

if ($IntervalSeconds -lt 1) {
    throw "IntervalSeconds must be 1 or greater."
}

$baseDir = $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($baseDir)) {
    $baseDir = (Get-Location).Path
}

$csvPath = Join-Path $baseDir "hardware_monitor.csv"

$counter = 0
$startTime = Get-Date

# ============================================================
# 2. Recursive sensor discovery
# ============================================================

function Get-SensorNodes {

    param(
        [Parameter(Mandatory = $true)]
        $Node,

        [string]$Parent = ""
    )

    $name = [string]$Node.Text
    $path = "$Parent/$name"

    if ($null -ne $Node.Value) {

        $value = [string]$Node.Value

        if (-not [string]::IsNullOrWhiteSpace($value)) {

            [PSCustomObject]@{
                Name  = $name
                Path  = $path
                Value = $value
                Min   = [string]$Node.Min
                Max   = [string]$Node.Max
            }
        }
    }

    foreach ($child in @($Node.Children)) {

        if ($null -ne $child) {
            Get-SensorNodes -Node $child -Parent $path
        }
    }
}

# ============================================================
# 3. Convert sensor value to numeric
# ============================================================

function Convert-SensorValue {

    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    if ($Value -match '(-?\d+(?:[.,]\d+)?)') {

        $number = $Matches[1].Replace(",", ".")

        return [double]::Parse(
            $number,
            [System.Globalization.CultureInfo]::InvariantCulture
        )
    }

    return $null
}

# ============================================================
# 4. Get all sensors
# ============================================================

function Get-AllSensors {

    param(
        [string]$ApiUrl
    )

    $data = Invoke-RestMethod `
        -Uri $ApiUrl `
        -TimeoutSec 5

    return @(
        Get-SensorNodes -Node $data
    )
}

# ============================================================
# 5. Detect temperature sensors
# ============================================================

function Get-TemperatureSensors {

    param(
        [array]$Sensors
    )

    return @(
        $Sensors | Where-Object {
            $_.Value -match '(?i)ÅãC|Åé|degC'
        }
    )
}

# ============================================================
# 6. Detect CPU temperature sensors
# ============================================================

function Get-CpuTemperatureSensors {

    param(
        [array]$Sensors
    )

    return @(
        $Sensors | Where-Object {

            $_.Path -match '(?i)CPU|Processor|Package|Core' -and
            $_.Value -match '(?i)ÅãC|Åé|degC'

        }
    )
}

# ============================================================
# 7. Detect CPU load sensor
# ============================================================

function Get-CpuLoad {

    param(
        [array]$Sensors
    )

    $cpuLoadSensor = $Sensors |
        Where-Object {

            $_.Path -match '(?i)CPU|Processor' -and
            $_.Value -match '%' -and
            $_.Name -match '(?i)CPU Total|Total CPU|CPU Usage|Total'

        } |
        Select-Object -First 1

    if ($null -ne $cpuLoadSensor) {

        return Convert-SensorValue $cpuLoadSensor.Value
    }

    return $null
}

# ============================================================
# 8. Detect storage temperature sensors
# ============================================================

function Get-StorageTemperatureSensors {

    param(
        [array]$Sensors
    )

    return @(
        $Sensors | Where-Object {

            $_.Value -match '(?i)ÅãC|Åé|degC' -and

            $_.Path -match '(?i)HDD|SSD|Storage|ST[0-9]|SAMSUNG|NVMe|WDC|Seagate|TOSHIBA|Kingston|Crucial'

        }
    )
}

# ============================================================
# 9. Initialize CSV file
# ============================================================

if (-not (Test-Path -LiteralPath $csvPath)) {

    "Timestamp,Category,Sensor,TemperatureC,MinC,MaxC,CpuLoadPercent" |
        Set-Content `
            -LiteralPath $csvPath `
            -Encoding UTF8
}

# ============================================================
# 10. Startup message
# ============================================================

Write-Host ""
Write-Host "================================================"
Write-Host " LibreHardwareMonitor - Hardware Monitor"
Write-Host "================================================"
Write-Host "API      : $Url"
Write-Host "Interval : $IntervalSeconds seconds"
Write-Host "CSV      : $csvPath"
Write-Host "Stop     : Ctrl+C"
Write-Host ""

# ============================================================
# 11. Initial API connection
# ============================================================

try {

    $allSensors = @(
        Get-AllSensors -ApiUrl $Url
    )

    Write-Host "[OK] HTTP API connected" `
        -ForegroundColor Green

}
catch {

    Write-Host "[ERROR] API connection failed" `
        -ForegroundColor Red

    Write-Host $_.Exception.Message

    exit 1
}

# ============================================================
# 12. Display all sensors (optional)
# ============================================================

if ($ShowAllSensors) {

    Write-Host ""
    Write-Host "=== All Sensors ==="

    $allSensors |
        Select-Object Path, Value, Min, Max |
        Format-Table -AutoSize -Wrap
}

# ============================================================
# 13. Initial sensor detection
# ============================================================

$cpuTemperatures = @(
    Get-CpuTemperatureSensors -Sensors $allSensors
)

$storageTemperatures = @(
    Get-StorageTemperatureSensors -Sensors $allSensors
)

$allTemperatures = @(
    Get-TemperatureSensors -Sensors $allSensors
)

$cpuLoad = Get-CpuLoad -Sensors $allSensors

Write-Host ""
Write-Host "=== Sensor Detection ==="

if ($cpuTemperatures.Count -gt 0) {

    Write-Host "[OK] CPU temperature sensors found" `
        -ForegroundColor Green

}
else {

    Write-Host "[WARNING] CPU temperature unavailable" `
        -ForegroundColor Yellow
}

if ($null -ne $cpuLoad) {

    Write-Host "[OK] CPU load sensor found" `
        -ForegroundColor Green

}
else {

    Write-Host "[WARNING] CPU load sensor unavailable" `
        -ForegroundColor Yellow
}

Write-Host "Storage temperature sensors: $($storageTemperatures.Count)"
Write-Host "All temperature sensors    : $($allTemperatures.Count)"

Write-Host ""
Write-Host "=== Available Temperature Sensors ==="

$allTemperatures |
    Select-Object Path, Value |
    Format-Table -AutoSize -Wrap

Write-Host ""
Write-Host "Monitoring started..."
Start-Sleep -Seconds 2

# ============================================================
# 14. Monitoring loop
# ============================================================

while ($true) {

    $counter++

    $timestamp = Get-Date

    try {

        # ----------------------------------------------------
        # 14.1 Read API
        # ----------------------------------------------------

        $allSensors = @(
            Get-AllSensors -ApiUrl $Url
        )

        # ----------------------------------------------------
        # 14.2 Detect sensors
        # ----------------------------------------------------

        $cpuTemperatures = @(
            Get-CpuTemperatureSensors -Sensors $allSensors
        )

        $storageTemperatures = @(
            Get-StorageTemperatureSensors -Sensors $allSensors
        )

        $allTemperatures = @(
            Get-TemperatureSensors -Sensors $allSensors
        )

        $cpuLoad = Get-CpuLoad -Sensors $allSensors

        # ----------------------------------------------------
        # 14.3 Display header
        # ----------------------------------------------------

        Clear-Host

        Write-Host "================================================"
        Write-Host " Hardware Temperature Monitor"
        Write-Host "================================================"

        Write-Host (
            "Time       : {0}" -f
            $timestamp.ToString("yyyy-MM-dd HH:mm:ss")
        )

        Write-Host "Samples    : $counter"

        $elapsed = (Get-Date) - $startTime

        Write-Host (
            "Elapsed    : {0:hh\:mm\:ss}" -f
            $elapsed
        )

        Write-Host "CSV        : $csvPath"

        Write-Host "------------------------------------------------"

        # ----------------------------------------------------
        # 14.4 CPU load
        # ----------------------------------------------------

        if ($null -ne $cpuLoad) {

            Write-Host (
                "CPU Load   : {0:N1} %" -f
                $cpuLoad
            )

        }
        else {

            Write-Host "CPU Load   : N/A" `
                -ForegroundColor Yellow
        }

        # ----------------------------------------------------
        # 14.5 CPU temperature
        # ----------------------------------------------------

        Write-Host ""
        Write-Host "=== CPU Temperature ==="

        if ($cpuTemperatures.Count -eq 0) {

            Write-Host "CPU Temp   : N/A" `
                -ForegroundColor Yellow

        }
        else {

            foreach ($sensor in $cpuTemperatures) {

                $temperature = Convert-SensorValue $sensor.Value

                if ($null -eq $temperature) {
                    continue
                }

                $color = "Green"

                if ($temperature -ge 85) {
                    $color = "Red"
                }
                elseif ($temperature -ge 70) {
                    $color = "Yellow"
                }

                Write-Host (
                    "{0,-30} {1,6:N1} C" -f
                    $sensor.Name,
                    $temperature
                ) -ForegroundColor $color
            }
        }

        # ----------------------------------------------------
        # 14.6 Storage temperature
        # ----------------------------------------------------

        Write-Host ""
        Write-Host "=== HDD / SSD Temperature ==="

        if ($storageTemperatures.Count -eq 0) {

            Write-Host "Storage temperature unavailable"

        }
        else {

            foreach ($sensor in $storageTemperatures) {

                $temperature = Convert-SensorValue $sensor.Value

                if ($null -eq $temperature) {
                    continue
                }

                Write-Host (
                    "{0,-30} {1,6:N1} C" -f
                    $sensor.Name,
                    $temperature
                )
            }
        }

        # ----------------------------------------------------
        # 14.7 Save CSV
        # ----------------------------------------------------

        foreach ($sensor in $allTemperatures) {

            $temperature = Convert-SensorValue $sensor.Value
            $minimum = Convert-SensorValue $sensor.Min
            $maximum = Convert-SensorValue $sensor.Max

            if ($null -eq $temperature) {
                continue
            }

            $category = "Other"

            if ($sensor.Path -match '(?i)CPU|Processor|Package|Core') {

                $category = "CPU"

            }
            elseif ($sensor.Path -match '(?i)HDD|SSD|Storage|ST[0-9]|SAMSUNG|NVMe|WDC|Seagate|TOSHIBA|Kingston|Crucial') {

                $category = "Storage"
            }

            $row = [PSCustomObject]@{

                Timestamp = $timestamp.ToString(
                    "yyyy-MM-dd HH:mm:ss.fff"
                )

                Category = $category

                Sensor = $sensor.Path

                TemperatureC = $temperature

                MinC = $minimum

                MaxC = $maximum

                CpuLoadPercent = $cpuLoad
            }

            $row |
                ConvertTo-Csv -NoTypeInformation |
                Select-Object -Skip 1 |
                Add-Content `
                    -LiteralPath $csvPath `
                    -Encoding UTF8
        }

        Write-Host ""
        Write-Host "------------------------------------------------"
        Write-Host "Ctrl+C to stop"

    }
    catch {

        Write-Host ""
        Write-Host "[ERROR] $($_.Exception.Message)" `
            -ForegroundColor Red

        Write-Host "Retrying..."
    }

    Start-Sleep -Seconds $IntervalSeconds
}