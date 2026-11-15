#requires -Version 5.1
<#
.SYNOPSIS
  LibreHardwareMonitor HTTP API -> SQLite (eight tables, GPU excluded).
.DESCRIPTION
  Stores all available non-GPU sensor readings in seven category tables,
  with one shared sensor_metadata table. Requires PSSQLite.
  Data is stored beside this script in hardware_monitor_8tables.db.
.EXAMPLE
  .\07_libreHardwareMonitor_8tables.ps1
.EXAMPLE
  .\07_libreHardwareMonitor_8tables.ps1 -ShowAllSensors -IntervalSeconds 5
.NOTES
  Install-Module PSSQLite -Scope CurrentUser
  Start LibreHardwareMonitor's Remote Web Server (default port 8085).
  Stop with Ctrl+C. Sampling interval is a post-cycle delay, not an exact clock.
#>
param(
    [string]$Url = 'http://127.0.0.1:8085/data.json',
    [ValidateRange(1,86400)][int]$IntervalSeconds = 1,
    [switch]$ShowAllSensors
)

$ErrorActionPreference = 'Stop'
Import-Module PSSQLite -ErrorAction Stop
$baseDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$dbPath = Join-Path $baseDir 'hardware_monitor_8tables.db'

# These names are known, trusted SQL identifiers (never supplied by the API).
$tableForCategory = @{
    CPU = 'cpu'; Memory = 'memory'; Storage = 'storage'
    Motherboard = 'motherboard'; Network = 'network'
    Battery = 'battery'; Other = 'other_sensors'
}
$measurementTables = @('cpu','memory','storage','motherboard','network','battery','other_sensors')
$gpuPattern = '(?i)(\bGPU\b|Graphics|GeForce|Radeon|\bNVIDIA\b|\bIntel Arc\b|\bDisplay Adapter\b|\bVideo Adapter\b)'
$script:sensorIdCache = @{}

function Get-SensorNodes {
    param([Parameter(Mandatory)]$Node, [string]$Parent = '')
    if ($null -eq $Node) { return }
    $name = [string]$Node.Text
    $path = "$Parent/$name"
    # Skip the whole GPU hardware branch, not just its individual readings.
    if ($name -match $script:gpuPattern) { return }
    $value = [string]$Node.Value
    if (-not [string]::IsNullOrWhiteSpace($value)) {
        [pscustomobject]@{
            Path = $path; Name = $name; RawValue = $value
            RawMin = [string]$Node.Min; RawMax = [string]$Node.Max
        }
    }
    foreach ($child in @($Node.Children)) {
        if ($null -ne $child) { Get-SensorNodes -Node $child -Parent $path }
    }
}

function Convert-SensorNumber {
    param([AllowNull()][string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return $null }
    if ($Text -match '^\s*(-?\d+(?:[.,]\d+)?)') {
        $s = $Matches[1].Replace(',', '.')
        return [double]::Parse($s, [Globalization.CultureInfo]::InvariantCulture)
    }
    return $null
}

function Get-SensorUnit {
    param([AllowNull()][string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return '' }
    return ($Text -replace '^\s*-?\d+(?:[.,]\d+)?\s*', '').Trim()
}

function Get-SensorCategory {
    param([string]$Path)
    # Prioritize physical hardware groups; all non-GPU nodes remain recordable.
    if ($Path -match '(?i)(\bCPU\b|\bProcessor\b|Intel Core|\bRyzen\b|\bXeon\b|\bPentium\b|\bCeleron\b)') { return 'CPU' }
    if ($Path -match '(?i)(\bMemory\b|\bRAM\b|\bDIMM\b)') { return 'Memory' }
    if ($Path -match '(?i)(\bHDD\b|\bSSD\b|Storage|NVMe|SAMSUNG|\bWDC\b|Seagate|Toshiba|Kingston|Crucial|Hard Disk|Disk Drive)') { return 'Storage' }
    if ($Path -match '(?i)(Network|Ethernet|Wi-Fi|Wireless|\bNIC\b)') { return 'Network' }
    if ($Path -match '(?i)(Battery|Batteries)') { return 'Battery' }
    if ($Path -match '(?i)(Motherboard|Mainboard|Super I/O|Nuvoton|Embedded Controller|\bITE\b)') { return 'Motherboard' }
    return 'Other'
}

function Invoke-Db {
    param(
        [Parameter(Mandatory)]$Connection,
        [Parameter(Mandatory)][string]$Query,
        [hashtable]$Parameters
    )
    if ($null -ne $Parameters) {
        return Invoke-SqliteQuery -SQLiteConnection $Connection -Query $Query -SqlParameters $Parameters
    }
    return Invoke-SqliteQuery -SQLiteConnection $Connection -Query $Query
}

function Initialize-Database {
    param([Parameter(Mandatory)]$Connection)
    Invoke-Db $Connection 'PRAGMA busy_timeout = 5000;' | Out-Null
    Invoke-Db $Connection 'PRAGMA foreign_keys = ON;' | Out-Null
    $metadataDdl = @'
CREATE TABLE IF NOT EXISTS sensor_metadata (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_path TEXT NOT NULL UNIQUE,
    sensor_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
'@
    Invoke-Db $Connection $metadataDdl | Out-Null
    foreach ($table in $script:measurementTables) {
        $ddl = @"
CREATE TABLE IF NOT EXISTS $table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    value REAL,
    min_value REAL,
    max_value REAL,
    raw_value TEXT,
    raw_min TEXT,
    raw_max TEXT,
    FOREIGN KEY(sensor_id) REFERENCES sensor_metadata(sensor_id)
);
"@
        Invoke-Db $Connection $ddl | Out-Null
        Invoke-Db $Connection "CREATE INDEX IF NOT EXISTS idx_${table}_sensor_time ON $table (sensor_id, timestamp);" | Out-Null
        Invoke-Db $Connection "CREATE INDEX IF NOT EXISTS idx_${table}_timestamp ON $table (timestamp);" | Out-Null
    }
}

function Get-OrCreateSensorId {
    param(
        [Parameter(Mandatory)]$Connection,
        [Parameter(Mandatory)]$Sensor,
        [Parameter(Mandatory)][string]$Category,
        [Parameter(Mandatory)][AllowEmptyString()][string]$Unit,
        [Parameter(Mandatory)][string]$Stamp
    )
    $path = [string]$Sensor.Path
    # Update metadata each time, including changing unit/category and last_seen.
    $metadataParams = @{
        path = $path; name = [string]$Sensor.Name
        category = $Category; unit = $Unit; stamp = $Stamp
    }
    $insertMetadata = @'
INSERT OR IGNORE INTO sensor_metadata
(sensor_path, sensor_name, category, unit, first_seen, last_seen)
VALUES (@path, @name, @category, @unit, @stamp, @stamp);
'@
    Invoke-Db -Connection $Connection -Query $insertMetadata -Parameters $metadataParams | Out-Null
    $updateMetadata = @'
UPDATE sensor_metadata
SET sensor_name = @name, category = @category, unit = @unit, last_seen = @stamp
WHERE sensor_path = @path;
'@
    Invoke-Db -Connection $Connection -Query $updateMetadata -Parameters $metadataParams | Out-Null

    if (-not $script:sensorIdCache.ContainsKey($path)) {
        $result = @(Invoke-Db $Connection 'SELECT sensor_id FROM sensor_metadata WHERE sensor_path = @path;' @{ path = $path })
        if ($result.Count -eq 0) { throw "Failed to register sensor: $path" }
        $script:sensorIdCache[$path] = [long]$result[0].sensor_id
    }
    return [long]$script:sensorIdCache[$path]
}

function Save-Sample {
    param([Parameter(Mandatory)][array]$Sensors, [Parameter(Mandatory)][string]$Stamp)
    $connection = New-SQLiteConnection -DataSource $script:dbPath
    $written = 0
    try {
        Invoke-Db $connection 'PRAGMA busy_timeout = 5000;' | Out-Null
        Invoke-Db $connection 'PRAGMA foreign_keys = ON;' | Out-Null
        Invoke-Db $connection 'BEGIN IMMEDIATE TRANSACTION;' | Out-Null
        try {
            foreach ($sensor in $Sensors) {
                $category = Get-SensorCategory ([string]$sensor.Path)
                $table = $script:tableForCategory[$category]
                $unit = Get-SensorUnit ([string]$sensor.RawValue)
                $sensorId = Get-OrCreateSensorId $connection $sensor $category $unit $Stamp
                $params = @{
                    sensor_id = $sensorId; stamp = $Stamp
                    value = (Convert-SensorNumber $sensor.RawValue)
                    min_value = (Convert-SensorNumber $sensor.RawMin)
                    max_value = (Convert-SensorNumber $sensor.RawMax)
                    raw_value = [string]$sensor.RawValue
                    raw_min = [string]$sensor.RawMin
                    raw_max = [string]$sensor.RawMax
                }
                $insert = @"
INSERT INTO $table
(sensor_id, timestamp, value, min_value, max_value, raw_value, raw_min, raw_max)
VALUES (@sensor_id, @stamp, @value, @min_value, @max_value, @raw_value, @raw_min, @raw_max);
"@
                Invoke-Db $connection $insert $params | Out-Null
                $written++
            }
            Invoke-Db $connection 'COMMIT;' | Out-Null
        } catch {
            try { Invoke-Db $connection 'ROLLBACK;' | Out-Null } catch { }
            throw
        }
    } finally {
        if ($null -ne $connection) { $connection.Dispose() }
    }
    return $written
}

# Initialize separately so an API failure does not prevent table creation.
$initConnection = New-SQLiteConnection -DataSource $dbPath
try { Initialize-Database -Connection $initConnection }
finally { if ($null -ne $initConnection) { $initConnection.Dispose() } }

Write-Host '=================================================='
Write-Host ' LibreHardwareMonitor -> SQLite (GPU EXCLUDED)'
Write-Host '=================================================='
Write-Host "Database : $dbPath"
Write-Host "API      : $Url"
Write-Host "Interval : $IntervalSeconds second(s) + execution time"
Write-Host 'Tables   : sensor_metadata, cpu, memory, storage,'
Write-Host '           motherboard, network, battery, other_sensors'
Write-Host 'Stop     : Ctrl+C'
Write-Host ''

$sampleCount = 0
while ($true) {
    $stamp = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ss.fffzzz')
    try {
        $root = Invoke-RestMethod -Uri $Url -TimeoutSec 5
        $sensors = @(Get-SensorNodes -Node $root)
        if ($sensors.Count -eq 0) {
            Write-Warning "[$stamp] No non-GPU sensor readings. SQLite unchanged."
        } else {
            $written = Save-Sample -Sensors $sensors -Stamp $stamp
            $sampleCount++
            $counts = $sensors | Group-Object { Get-SensorCategory $_.Path } | ForEach-Object { "$($_.Name)=$($_.Count)" }
            Write-Host ("[{0}] Sample={1} Written={2}  {3}" -f $stamp,$sampleCount,$written,($counts -join ' '))
            if ($ShowAllSensors) {
                $sensors | Select-Object Path, RawValue, RawMin, RawMax | Format-Table -AutoSize -Wrap
            }
        }
    } catch {
        Write-Warning "[$stamp] API/SQLite error: $($_.Exception.Message). Retrying next cycle."
    }
    Start-Sleep -Seconds $IntervalSeconds
}
