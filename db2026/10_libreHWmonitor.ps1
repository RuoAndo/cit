
# ============================================================
# 07_libreHardwareMonitor.ps1
#
# LibreHardwareMonitor - Hardware Monitor (No GPU)
#
# Windows PowerShell 5.1 / PowerShell 7
#
# Features:
#   - Exclude all GPU sensors
#   - Automatically discover hardware sensors
#   - Monitor CPU, memory, storage, motherboard,
#     network and battery sensors
#   - Display current / min / max values
#   - Save all available sensor readings to CSV
#   - Continue when individual sensors are unavailable
#   - Reconnect automatically when HTTP API fails
#   - Show all sensor readings
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

$csvPath = Join-Path $baseDir "hardware_monitor_no_gpu.csv"

$counter = 0
$startTime = Get-Date

# GPU-related path names.
# The GPU branch is excluded before recursion.
$gpuPattern = '(?i)(GPU|Graphics|GeForce|Radeon|Intel\(R\).*Graphics|Arc Graphics|Display Adapter)'

# ============================================================
# 2. Recursive sensor discovery
# ============================================================

function Get-SensorNodes {

    param(
        [Parameter(Mandatory = $true)]
        $Node,

        [string]$Parent = "",

        [string]$GpuPattern = $script:gpuPattern
    )

    if ($null -eq $Node) {
        return
    }

    $name = [string]$Node.Text
    $path = "$Parent/$name"

    # Skip the entire GPU subtree.
    if ($path -match $GpuPattern) {
        return
    }

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

    foreach ($child in @($Node.Children)) {

        if ($null -ne $child) {

            Get-SensorNodes `
                -Node $child `
                -Parent $path `
                -GpuPattern $GpuPattern
        }
    }
}

# ============================================================
# 3. Convert a sensor value to a number
# ============================================================

function Convert-SensorValue {

    param(
        [AllowNull()]
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    # Extract the first numeric value.
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
# 4. Detect measurement units
# ============================================================

function Get-SensorUnit {

    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }

    $unit = $Value -replace '^\s*-?\d+(?:[.,]\d+)?\s*', ''

    return $unit.Trim()
}

# ============================================================
# 5. Classify hardware sensors
# ============================================================

function Get-SensorCategory {

    param(
        [string]$Path
    )

    if ($Path -match '(?i)CPU|Processor|Intel Core|Ryzen|Xeon') {
        return "CPU"
    }

    if ($Path -match '(?i)Memory|RAM|Virtual Memory|Physical Memory') {
        return "Memory"
    }

    if ($Path -match '(?i)HDD|SSD|Storage|NVMe|Samsung|WDC|Seagate|TOSHIBA|Kingston|Crucial|Hard Disk|Drive') {
        return "Storage"
    }

    if ($Path -match '(?i)Network|Ethernet|Wi-Fi|Wireless|Adapter') {
        return "Network"
    }

    if ($Path -match '(?i)Battery') {
        return "Battery"
    }

    if ($Path -match '(?i)Motherboard|Mainboard|Super I/O|Nuvoton|ITE|EC|Embedded Controller') {
        return "Motherboard"
    }

    return "Other"
}

# ============================================================
# 6. Read all available sensors from the HTTP API
# ============================================================

function Get-AllSensors {

    param(
        [string]$ApiUrl
    )

    $data = Invoke-RestMethod `
        -Uri $ApiUrl `
        -TimeoutSec 5

    return @(
        Get-SensorNodes `
            -Node $data `
            -GpuPattern $script:gpuPattern
    )
}

# ============================================================
# 7. Detect CPU load
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
# 8. CSV initialization
# ============================================================

$csvColumns = @(
    "Timestamp",
    "Category",
    "Sensor",
    "SensorName",
    "Value",
    "Unit",
    "Min",
    "Max",
    "RawValue",
    "RawMin",
    "RawMax"
)

# Create the file if it does not exist.
if (-not (Test-Path -LiteralPath $csvPath)) {

    $header = $csvColumns -join ","

    Set-Content `
        -LiteralPath $csvPath `
        -Value $header `
        -Encoding UTF8
}

# ============================================================
# 9. Startup information
# ============================================================

Write-Host ""
Write-Host "================================================"
Write-Host " LibreHardwareMonitor - Hardware Monitor"
Write-Host " GPU Sensors: EXCLUDED"
Write-Host "================================================"

Write-Host "API      : $Url"
Write-Host "Interval : $IntervalSeconds seconds"
Write-Host "CSV      : $csvPath"
Write-Host "Stop     : Ctrl+C"
Write-Host ""

# ============================================================
# 10. Initial connection
# ============================================================

try {

    $allSensors = @(
        Get-AllSensors -ApiUrl $Url
    )

    Write-Host "[OK] HTTP API connected" `
        -ForegroundColor Green

}
catch {

    Write-Host "[WARNING] Initial API connection failed" `
        -ForegroundColor Yellow

    Write-Host $_.Exception.Message
    Write-Host "The monitoring loop will retry."
    Write-Host ""

    $allSensors = @()
}

# ============================================================
# 11. Initial sensor listing
# ============================================================

Write-Host ""
Write-Host "=== Initial Sensor Detection (GPU Excluded) ==="

Write-Host "Available sensors: $($allSensors.Count)"

if ($ShowAllSensors) {

    Write-Host ""
    Write-Host "=== All Available Sensors ==="

    $allSensors |
        Select-Object Path, Value, Min, Max |
        Format-Table -AutoSize -Wrap
}

Write-Host ""
Write-Host "Monitoring started..."
Start-Sleep -Seconds 2

# ============================================================
# 12. Monitoring loop
# ============================================================

while ($true) {

    $timestamp = Get-Date

    try {

        # ----------------------------------------------------
        # 12.1 Read sensor data
        # ----------------------------------------------------

        $allSensors = @(
            Get-AllSensors -ApiUrl $Url
        )

        $counter++

        # ----------------------------------------------------
        # 12.2 Display header
        # ----------------------------------------------------

        Clear-Host

        Write-Host "================================================"
        Write-Host " Hardware Monitor (GPU Excluded)"
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

        Write-Host "Sensors    : $($allSensors.Count)"
        Write-Host "CSV        : $csvPath"
        Write-Host "GPU        : Excluded"

        # ----------------------------------------------------
        # 12.3 CPU load
        # ----------------------------------------------------

        $cpuLoad = Get-CpuLoad -Sensors $allSensors

        Write-Host ""
        Write-Host "=== CPU Load ==="

        if ($null -ne $cpuLoad) {

            Write-Host (
                "CPU Total : {0:N1} %" -f $cpuLoad
            )
        }
        else {

            Write-Host "CPU Total : N/A" `
                -ForegroundColor Yellow
        }

        # ----------------------------------------------------
        # 12.4 Group sensors
        # ----------------------------------------------------

        $groupedSensors = @(
            $allSensors |
                Group-Object {
                    Get-SensorCategory -Path $_.Path
                } |
                Sort-Object Name
        )

        foreach ($group in $groupedSensors) {

            Write-Host ""
            Write-Host "=== $($group.Name) ==="

            foreach ($sensor in $group.Group) {

                $displayValue = [string]$sensor.Value

                $numericValue = Convert-SensorValue $displayValue

                $color = "Gray"

                # Color CPU temperatures only.
                if (
                    $group.Name -eq "CPU" -and
                    $displayValue -match '(?i)ÅãC|Åé|degC' -and
                    $null -ne $numericValue
                ) {

                    if ($numericValue -ge 85) {
                        $color = "Red"
                    }
                    elseif ($numericValue -ge 70) {
                        $color = "Yellow"
                    }
                    else {
                        $color = "Green"
                    }
                }

                $line = "{0,-35} {1,15}" -f `
                    $sensor.Name,
                    $displayValue

                Write-Host $line -ForegroundColor $color
            }
        }

        # ----------------------------------------------------
        # 12.5 Prepare CSV rows
        # ----------------------------------------------------

        $csvRows = @(
            foreach ($sensor in $allSensors) {

                $category = Get-SensorCategory -Path $sensor.Path

                $value = Convert-SensorValue $sensor.Value
                $minimum = Convert-SensorValue $sensor.Min
                $maximum = Convert-SensorValue $sensor.Max

                $unit = Get-SensorUnit -Value $sensor.Value

                [PSCustomObject][ordered]@{

                    Timestamp = $timestamp.ToString(
                        "yyyy-MM-dd HH:mm:ss.fff"
                    )

                    Category = $category

                    Sensor = $sensor.Path

                    SensorName = $sensor.Name

                    Value = $value

                    Unit = $unit

                    Min = $minimum

                    Max = $maximum

                    RawValue = $sensor.Value

                    RawMin = $sensor.Min

                    RawMax = $sensor.Max
                }
            }
        )

        # ----------------------------------------------------
        # 12.6 Write CSV
        # ----------------------------------------------------

        if ($csvRows.Count -gt 0) {

            # ConvertTo-Csv uses invariant property ordering.
            $csvLines = @(
                $csvRows |
                    ConvertTo-Csv -NoTypeInformation |
                    Select-Object -Skip 1
            )

            Add-Content `
                -LiteralPath $csvPath `
                -Value $csvLines `
                -Encoding UTF8
        }

        # ----------------------------------------------------
        # 12.7 Status
        # ----------------------------------------------------

        Write-Host ""
        Write-Host "------------------------------------------------"

        Write-Host (
            "Saved rows : {0}" -f $csvRows.Count
        ) -ForegroundColor Green

        Write-Host "GPU sensors were excluded."

        Write-Host "Ctrl+C to stop"

    }
    catch {

        Write-Host ""
        Write-Host "[ERROR] $($_.Exception.Message)" `
            -ForegroundColor Red

        Write-Host "Reconnecting to LibreHardwareMonitor..."
    }

    # --------------------------------------------------------
    # 12.8 Wait
    # --------------------------------------------------------

    Start-Sleep -Seconds $IntervalSeconds
}
