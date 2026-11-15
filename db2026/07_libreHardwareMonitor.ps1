
# ============================================================
# 07_libreHardwareMonitor.ps1
#
# LibreHardwareMonitor HTTP API
# CPU Temperature / CPU Load Monitor
#
# Windows PowerShell 5.1 / PowerShell 7
# Ctrl+C で停止
# ============================================================

param(
    [string]$Url = "http://127.0.0.1:8085/data.json",
    [int]$IntervalSeconds = 1,
    [switch]$ShowAllSensors
)

$ErrorActionPreference = "Stop"

# CSV保存先：スクリプトと同じフォルダ
$baseDir = $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($baseDir)) {
    $baseDir = (Get-Location).Path
}

$csvPath = Join-Path $baseDir "cpu_temperature.csv"

# ------------------------------------------------------------
# 1. センサー階層を再帰的に取得
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# 2. 温度などの数値を取り出す
# ------------------------------------------------------------

function Convert-SensorValue {
    param(
        [string]$Value
    )

    if ($Value -match '(-?\d+(?:[.,]\d+)?)') {
        $number = $Matches[1].Replace(",", ".")

        return [double]::Parse(
            $number,
            [System.Globalization.CultureInfo]::InvariantCulture
        )
    }

    return $null
}

# ------------------------------------------------------------
# 3. API接続確認
# ------------------------------------------------------------

Write-Host ""
Write-Host "==============================================="
Write-Host " LibreHardwareMonitor - CPU Monitor"
Write-Host "==============================================="
Write-Host "API      : $Url"
Write-Host "Interval : $IntervalSeconds seconds"
Write-Host "CSV      : $csvPath"
Write-Host "Stop     : Ctrl+C"
Write-Host ""

if ($IntervalSeconds -lt 1) {
    throw "IntervalSeconds は1以上にしてください。"
}

try {
    $data = Invoke-RestMethod -Uri $Url -TimeoutSec 5
    Write-Host "[OK] HTTP API connected" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] API connection failed" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

# ------------------------------------------------------------
# 4. センサー一覧
# ------------------------------------------------------------

$allSensors = @(
    Get-SensorNodes -Node $data
)

if ($ShowAllSensors) {
    Write-Host ""
    Write-Host "=== All Sensors ==="

    $allSensors |
        Select-Object Path, Value, Min, Max |
        Format-Table -AutoSize -Wrap
}

# ------------------------------------------------------------
# 5. CPU温度センサーを検出
# ------------------------------------------------------------

$cpuTemperatureSensors = @(
    $allSensors |
        Where-Object {
            $_.Path -match '(?i)CPU|Processor|Package|Core' -and
            $_.Value -match '(?i)°C|℃|degC'
        }
)

Write-Host ""
Write-Host "=== Detected CPU Temperature Sensors ==="

if ($cpuTemperatureSensors.Count -eq 0) {

    Write-Host "[WARNING] CPU temperature sensor not found" `
        -ForegroundColor Yellow

    Write-Host ""
    Write-Host "=== Available Temperature Sensors ==="

    $allSensors |
        Where-Object {
            $_.Value -match '(?i)°C|℃|degC'
        } |
        Select-Object Path, Value |
        Format-Table -AutoSize -Wrap

    Write-Host ""
    Write-Host "CPUセンサーを確認してください。"
    exit 1
}

$cpuTemperatureSensors |
    Select-Object Name, Value, Min, Max, Path |
    Format-Table -AutoSize

# ------------------------------------------------------------
# 6. CSVヘッダー準備
# ------------------------------------------------------------

if (-not (Test-Path -LiteralPath $csvPath)) {

    "Timestamp,Sensor,TemperatureC,MinC,MaxC,CpuLoadPercent" |
        Set-Content -LiteralPath $csvPath -Encoding UTF8
}

# ------------------------------------------------------------
# 7. 監視開始
# ------------------------------------------------------------

$counter = 0
$startTime = Get-Date

while ($true) {

    $counter++
    $timestamp = Get-Date

    try {
        $data = Invoke-RestMethod -Uri $Url -TimeoutSec 5

        $allSensors = @(
            Get-SensorNodes -Node $data
        )

        # CPU温度抽出
        $temperatures = @(
            $allSensors |
                Where-Object {
                    $_.Path -match '(?i)CPU|Processor|Package|Core' -and
                    $_.Value -match '(?i)°C|℃|degC'
                }
        )

        # CPU使用率抽出
        $cpuLoad = $allSensors |
            Where-Object {
                $_.Path -match '(?i)CPU|Processor' -and
                $_.Name -match '(?i)CPU Total|Total CPU|CPU Usage'
                -and $_.Value -match '%'
            } |
            Select-Object -First 1

        $cpuLoadValue = $null

        if ($null -ne $cpuLoad) {
            $cpuLoadValue = Convert-SensorValue $cpuLoad.Value
        }

        Clear-Host

        Write-Host "==============================================="
        Write-Host " CPU Temperature Monitor"
        Write-Host "==============================================="
        Write-Host "Time    : $($timestamp.ToString('yyyy-MM-dd HH:mm:ss'))"
        Write-Host "Samples : $counter"
        Write-Host "CSV     : $csvPath"

        if ($null -ne $cpuLoadValue) {
            Write-Host ("CPU Load: {0:N1} %" -f $cpuLoadValue)
        }

        Write-Host "-----------------------------------------------"

        foreach ($sensor in $temperatures) {

            $temperature = Convert-SensorValue $sensor.Value
            $minimum = Convert-SensorValue $sensor.Min
            $maximum = Convert-SensorValue $sensor.Max

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
                "{0,-25} {1,6:N1} C" -f
                $sensor.Name,
                $temperature
            ) -ForegroundColor $color

            # CSV書き込み
            $row = [PSCustomObject]@{
                Timestamp      = $timestamp.ToString("yyyy-MM-dd HH:mm:ss.fff")
                Sensor         = $sensor.Path
                TemperatureC   = $temperature
                MinC           = $minimum
                MaxC           = $maximum
                CpuLoadPercent = $cpuLoadValue
            }

            $row |
                ConvertTo-Csv -NoTypeInformation |
                Select-Object -Skip 1 |
                Add-Content -LiteralPath $csvPath -Encoding UTF8
        }

        if ($temperatures.Count -eq 0) {
            Write-Host "[WARNING] CPU sensors not found" `
                -ForegroundColor Yellow
        }

        Write-Host "-----------------------------------------------"
        Write-Host "Ctrl+C to stop"
    }
    catch {
        Write-Host "[ERROR] $($_.Exception.Message)" `
            -ForegroundColor Red
    }

    Start-Sleep -Seconds $IntervalSeconds
}
