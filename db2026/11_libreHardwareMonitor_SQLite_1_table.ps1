# LibreHardwareMonitor -> SQLite (GPU excluded)
# Windows PowerShell 5.1 / PowerShell 7
# Requires: Install-Module PSSQLite -Scope CurrentUser
param(
    [string]$Url = 'http://127.0.0.1:8085/data.json',
    [int]$IntervalSeconds = 1,
    [switch]$ShowAllSensors
)
$ErrorActionPreference = 'Stop'
if ($IntervalSeconds -lt 1) { throw 'IntervalSeconds must be >= 1.' }
Import-Module PSSQLite -ErrorAction Stop
$baseDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$dbPath = Join-Path $baseDir 'hardware_monitor.db'
# Filter entire graphics-device branches, rather than filtering only sensor names.
$gpuPattern = '(?i)GPU|Graphics|GeForce|Radeon|NVIDIA|Intel\(R\) Arc|Display Adapter'

function Get-SensorNodes {
    param($Node, [string]$Parent = '')
    if ($null -eq $Node) { return }
    $name = [string]$Node.Text
    $path = "$Parent/$name"
    if ($path -match $script:gpuPattern) { return }
    $value = [string]$Node.Value
    if (-not [string]::IsNullOrWhiteSpace($value)) {
        [pscustomobject]@{
            Path = $path; Name = $name; Value = $value
            Min = [string]$Node.Min; Max = [string]$Node.Max
        }
    }
    foreach ($child in @($Node.Children)) {
        if ($null -ne $child) { Get-SensorNodes -Node $child -Parent $path }
    }
}
function Convert-SensorValue {
    param([AllowNull()][string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return $null }
    if ($Text -match '^\s*(-?\d+(?:[.,]\d+)?)') {
        $s = $Matches[1].Replace(',', '.')
        return [double]::Parse($s, [Globalization.CultureInfo]::InvariantCulture)
    }
    return $null
}
function Get-Unit {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return '' }
    return ($Text -replace '^\s*-?\d+(?:[.,]\d+)?\s*', '').Trim()
}
function Get-Category {
    param([string]$Path)
    if ($Path -match '(?i)CPU|Processor|Intel Core|Ryzen|Xeon') { return 'CPU' }
    if ($Path -match '(?i)Memory|RAM') { return 'Memory' }
    if ($Path -match '(?i)HDD|SSD|Storage|NVMe|Samsung|WDC|Seagate|Toshiba|Kingston|Crucial|Hard Disk') { return 'Storage' }
    if ($Path -match '(?i)Network|Ethernet|Wi-Fi|Wireless') { return 'Network' }
    if ($Path -match '(?i)Battery') { return 'Battery' }
    if ($Path -match '(?i)Motherboard|Mainboard|Super I/O|Nuvoton|Embedded Controller') { return 'Motherboard' }
    return 'Other'
}

$schema = @'
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    category TEXT NOT NULL,
    sensor_path TEXT NOT NULL,
    sensor_name TEXT NOT NULL,
    value REAL,
    unit TEXT,
    min_value REAL,
    max_value REAL,
    raw_value TEXT,
    raw_min TEXT,
    raw_max TEXT
);
CREATE INDEX IF NOT EXISTS ix_sensor_time
ON sensor_readings (sensor_path, timestamp);
CREATE INDEX IF NOT EXISTS ix_time ON sensor_readings (timestamp);
'@
Invoke-SqliteQuery -DataSource $dbPath -Query $schema | Out-Null
$insert = @'
INSERT INTO sensor_readings
(timestamp,category,sensor_path,sensor_name,value,unit,min_value,max_value,raw_value,raw_min,raw_max)
VALUES (@ts,@category,@path,@name,@value,@unit,@min,@max,@raw_value,@raw_min,@raw_max);
'@

Write-Host "Database : $dbPath"
Write-Host "API      : $Url"
Write-Host 'GPU      : excluded'
Write-Host 'Stop     : Ctrl+C'
$count = 0
while ($true) {
    try {
        $stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss.fff')
        $root = Invoke-RestMethod -Uri $Url -TimeoutSec 5
        $sensors = @(Get-SensorNodes -Node $root)
        if ($sensors.Count -eq 0) {
            Write-Warning 'No non-GPU sensor values were returned.'
        } else {
            # One connection and one transaction per collection cycle.
            $conn = New-SQLiteConnection -DataSource $dbPath
            try {
                Invoke-SqliteQuery -SQLiteConnection $conn -Query 'BEGIN TRANSACTION;' | Out-Null
                try {
                    foreach ($sensor in $sensors) {
                        $params = @{
                            ts = $stamp
                            category = (Get-Category $sensor.Path)
                            path = $sensor.Path
                            name = $sensor.Name
                            value = (Convert-SensorValue $sensor.Value)
                            unit = (Get-Unit $sensor.Value)
                            min = (Convert-SensorValue $sensor.Min)
                            max = (Convert-SensorValue $sensor.Max)
                            raw_value = $sensor.Value
                            raw_min = $sensor.Min
                            raw_max = $sensor.Max
                        }
                        Invoke-SqliteQuery -SQLiteConnection $conn -Query $insert -SqlParameters $params | Out-Null
                    }
                    Invoke-SqliteQuery -SQLiteConnection $conn -Query 'COMMIT;' | Out-Null
                } catch {
                    Invoke-SqliteQuery -SQLiteConnection $conn -Query 'ROLLBACK;' | Out-Null
                    throw
                }
            } finally {
                if ($null -ne $conn) { $conn.Dispose() }
            }
        }
        $count++
        Write-Host ("[{0}] Sample={1} Stored={2} sensors" -f $stamp, $count, $sensors.Count)
        if ($ShowAllSensors) {
            $sensors | Select-Object Path, Value, Min, Max | Format-Table -AutoSize -Wrap
        }
    } catch {
        Write-Warning "Acquisition or save failed: $($_.Exception.Message). Retrying."
    }
    Start-Sleep -Seconds $IntervalSeconds
}
