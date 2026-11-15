#requires -Version 5.1
<#
.SYNOPSIS
 Import LibreHardwareMonitor CSV files into the existing 8-table SQLite DB.
.DESCRIPTION
 Imports hardware_sensor_readings.csv into sensor_metadata and seven measurement
 tables; hardware_monitor_cycles.csv and hardware_monitor_errors.csv into two
 additional tables (10 total). GPU readings are always excluded.
 Avoids duplicates when run again on the same CSV files.
 Requires PSSQLite; compatible with Windows PowerShell 5.1 / PowerShell 7.
.EXAMPLE
 .\13_import_HardwareCSV_to_SQLite.ps1
.EXAMPLE
 .\13_import_HardwareCSV_to_SQLite.ps1 -CsvDir 'D:\cit\db2026' -ShowEachRow
.EXAMPLE
 .\13_import_HardwareCSV_to_SQLite.ps1 -DbPath 'D:\cit\db2026\hardware_monitor_8tables.db'
#>
param(
    [string]$CsvDir = '',
    [string]$DbPath = '',
    [switch]$ShowEachRow,
    [ValidateRange(1,1000000)][int]$ProgressEvery = 25
)

$ErrorActionPreference = 'Stop'
Import-Module PSSQLite -ErrorAction Stop
$baseDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
if ([string]::IsNullOrWhiteSpace($CsvDir)) { $CsvDir = $baseDir }
if ([string]::IsNullOrWhiteSpace($DbPath)) { $DbPath = Join-Path $baseDir 'hardware_monitor_8tables.db' }
$CsvDir = [IO.Path]::GetFullPath($CsvDir)
$DbPath = [IO.Path]::GetFullPath($DbPath)
if (-not (Test-Path -LiteralPath $CsvDir -PathType Container)) { throw "CSV directory not found: $CsvDir" }
$dbDir = Split-Path -Parent $DbPath
if (-not (Test-Path -LiteralPath $dbDir -PathType Container)) { throw "Database directory not found: $dbDir" }

$readingsFile = Join-Path $CsvDir 'hardware_sensor_readings.csv'
$cyclesFile   = Join-Path $CsvDir 'hardware_monitor_cycles.csv'
$errorsFile   = Join-Path $CsvDir 'hardware_monitor_errors.csv'
$gpuPattern = '(?i)(\bGPU\b|Graphics|GeForce|Radeon|\bNVIDIA\b|\bIntel Arc\b|\bDisplay Adapter\b|\bVideo Adapter\b)'
$tableForCategory = @{
    CPU='cpu'; Memory='memory'; Storage='storage'; Motherboard='motherboard'
    Network='network'; Battery='battery'; Other='other_sensors'
}
$measurementTables = @('cpu','memory','storage','motherboard','network','battery','other_sensors')
$logPath = Join-Path $CsvDir ('hardware_import_' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.log')
$script:logPath = $logPath

function Write-Step {
    param([string]$Stage,[string]$Message,[string]$Color='Gray')
    $line = ('[{0}] [{1,-11}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'),$Stage,$Message)
    Write-Host $line -ForegroundColor $Color
    Add-Content -LiteralPath $script:logPath -Value $line -Encoding UTF8
}
function Invoke-Db {
    param($Connection,[string]$Query,[hashtable]$Parameters)
    if ($null -ne $Parameters) {
        Invoke-SqliteQuery -SQLiteConnection $Connection -Query $Query -SqlParameters $Parameters
    } else {
        Invoke-SqliteQuery -SQLiteConnection $Connection -Query $Query
    }
}
function To-NullableNumber {
    param([AllowNull()][string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return $null }
    $number = 0.0
    $s = $Text.Trim().Replace(',','.')
    if ([double]::TryParse($s, [Globalization.NumberStyles]::Float,
            [Globalization.CultureInfo]::InvariantCulture, [ref]$number)) { return $number }
    if ($s -match '^\s*(-?\d+(?:\.\d+)?)') {
        return [double]::Parse($Matches[1],[Globalization.CultureInfo]::InvariantCulture)
    }
    return $null
}
function Get-Category {
    param([string]$Path,[string]$CsvCategory)
    # Use original CSV category first, preserving the monitor's classification.
    $known = @('CPU','Memory','Storage','Motherboard','Network','Battery','Other')
    foreach ($k in $known) { if ($CsvCategory -ieq $k) { return $k } }
    if ($Path -match '(?i)(\bCPU\b|\bProcessor\b|Intel Core|\bRyzen\b|\bXeon\b|\bPentium\b|\bCeleron\b)') { return 'CPU' }
    if ($Path -match '(?i)(\bMemory\b|\bRAM\b|\bDIMM\b)') { return 'Memory' }
    if ($Path -match '(?i)(\bHDD\b|\bSSD\b|Storage|NVMe|SAMSUNG|\bWDC\b|Seagate|Toshiba|Kingston|Crucial|Hard Disk|Disk Drive)') { return 'Storage' }
    if ($Path -match '(?i)(Network|Ethernet|Wi-Fi|Wireless|\bNIC\b)') { return 'Network' }
    if ($Path -match '(?i)(Battery|Batteries)') { return 'Battery' }
    if ($Path -match '(?i)(Motherboard|Mainboard|Super I/O|Nuvoton|Embedded Controller|\bITE\b)') { return 'Motherboard' }
    return 'Other'
}
function Verify-Columns {
    param([array]$Rows,[string[]]$Required,[string]$Name)
    if ($Rows.Count -eq 0) { return }
    $names = @($Rows[0].PSObject.Properties.Name)
    foreach ($col in $Required) {
        if ($names -notcontains $col) { throw "$Name : missing CSV column '$col'. Actual columns: $($names -join ', ')" }
    }
}
function Initialize-Database {
    param($Connection)
    Invoke-Db $Connection 'PRAGMA busy_timeout=10000;' | Out-Null
    Invoke-Db $Connection 'PRAGMA foreign_keys=ON;' | Out-Null
    Invoke-Db $Connection @'
CREATE TABLE IF NOT EXISTS sensor_metadata (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_path TEXT NOT NULL UNIQUE,
    sensor_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
'@ | Out-Null
    foreach ($table in $script:measurementTables) {
        $ddl = @"
CREATE TABLE IF NOT EXISTS $table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    value REAL, min_value REAL, max_value REAL,
    raw_value TEXT, raw_min TEXT, raw_max TEXT,
    FOREIGN KEY(sensor_id) REFERENCES sensor_metadata(sensor_id)
);
"@
        Invoke-Db $Connection $ddl | Out-Null
        Invoke-Db $Connection "CREATE INDEX IF NOT EXISTS idx_${table}_sensor_time ON $table (sensor_id,timestamp);" | Out-Null
    }
    Invoke-Db $Connection @'
CREATE TABLE IF NOT EXISTS monitor_cycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    sample_number INTEGER,
    status TEXT,
    api_ms REAL, sqlite_ms REAL, csv_ms REAL, total_ms REAL,
    detected INTEGER, written_sqlite INTEGER, written_csv INTEGER,
    cpu INTEGER, memory INTEGER, storage INTEGER, motherboard INTEGER,
    network INTEGER, battery INTEGER, other_sensors INTEGER,
    error_message TEXT
);
'@ | Out-Null
    Invoke-Db $Connection 'CREATE INDEX IF NOT EXISTS idx_monitor_cycles_stamp ON monitor_cycles(timestamp,sample_number);' | Out-Null
    Invoke-Db $Connection @'
CREATE TABLE IF NOT EXISTS monitor_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    sample_number INTEGER,
    stage TEXT,
    message TEXT,
    exception_type TEXT
);
'@ | Out-Null
    Invoke-Db $Connection 'CREATE INDEX IF NOT EXISTS idx_monitor_errors_stamp ON monitor_errors(timestamp,sample_number);' | Out-Null
}

$files = @(
    @{ Kind='Readings'; Path=$readingsFile },
    @{ Kind='Cycles';   Path=$cyclesFile },
    @{ Kind='Errors';   Path=$errorsFile }
)
Write-Host '============================================================'
Write-Host ' Hardware CSV -> SQLite | 10 tables | GPU EXCLUDED'
Write-Host '============================================================'
Write-Step 'DIRECTORY' $CsvDir 'Cyan'
Write-Step 'DATABASE' $DbPath 'Cyan'
Write-Step 'LOG FILE' $logPath 'Cyan'
Write-Step 'SETTINGS' "ProgressEvery=$ProgressEvery; ShowEachRow=$ShowEachRow; GPU=excluded" 'Cyan'
foreach ($file in $files) {
    if (Test-Path -LiteralPath $file.Path -PathType Leaf) {
        Write-Step 'CSV FOUND' $file.Path 'Green'
    } else {
        Write-Step 'CSV MISSING' "$($file.Path) (skipped)" 'Yellow'
    }
}
Write-Host ''

$connection = $null
$watch = [Diagnostics.Stopwatch]::StartNew()
$counts = [ordered]@{ Imported=0; Duplicate=0; GpuSkipped=0; Invalid=0; Failed=0 }
$perTable = @{}
foreach ($t in $measurementTables + @('monitor_cycles','monitor_errors')) { $perTable[$t] = 0 }
$cache = @{}
try {
    Write-Step 'DB CONNECT' 'Opening SQLite connection...' 'Cyan'
    $connection = New-SQLiteConnection -DataSource $DbPath
    Write-Step 'DB SCHEMA' 'Checking/creating the 10 SQLite tables and indexes...' 'Cyan'
    Initialize-Database $connection
    Write-Step 'DB READY' '8 original tables + monitor_cycles + monitor_errors' 'Green'

    foreach ($file in $files) {
        if (-not (Test-Path -LiteralPath $file.Path -PathType Leaf)) { continue }
        Write-Host ''
        Write-Step 'IMPORT' "Type=$($file.Kind) / $($file.Path)" 'Cyan'
        $fileWatch = [Diagnostics.Stopwatch]::StartNew()
        $csvInfo = Get-Item -LiteralPath $file.Path
        Write-Step 'CSV SIZE' ("{0:N0} bytes | modified={1}" -f $csvInfo.Length, $csvInfo.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')) 'Gray'
        Write-Step 'CSV READ' 'Reading UTF-8 CSV...' 'Gray'
        $rows = @(Import-Csv -LiteralPath $file.Path -Encoding UTF8)
        switch ($file.Kind) {
            'Readings' { Verify-Columns $rows @('timestamp','category','sensor_path','sensor_name','unit','raw_value','raw_min','raw_max') $file.Path }
            'Cycles' { Verify-Columns $rows @('timestamp','sample_number','status') $file.Path }
            'Errors' { Verify-Columns $rows @('timestamp','sample_number','stage','message') $file.Path }
        }
        Write-Step 'ROWS' "Read $($rows.Count) CSV rows; validating required columns OK" 'White'
        $beforeImported = $counts.Imported
        $beforeDup = $counts.Duplicate
        $beforeGpu = $counts.GpuSkipped
        $beforeInvalid = $counts.Invalid
        $fileInserted = @{}
        foreach ($t in $measurementTables + @('monitor_cycles','monitor_errors')) { $fileInserted[$t] = 0 }
        $i = 0
        $importedHere = 0
        $skippedHere = 0
        # One transaction per source file; failure rolls back this file only.
        Write-Step 'SQL BEGIN' 'Starting transaction (entire CSV is atomic)...' 'Cyan'
        Invoke-Db $connection 'BEGIN IMMEDIATE TRANSACTION;' | Out-Null
        try {
            foreach ($r in $rows) {
                $i++
                try {
                $stamp = [string]$r.timestamp
                if ([string]::IsNullOrWhiteSpace($stamp)) { $counts.Invalid++; $skippedHere++; continue }
                $table = ''
                if ($file.Kind -eq 'Readings') {
                    $path = [string]$r.sensor_path
                    if ([string]::IsNullOrWhiteSpace($path)) { $counts.Invalid++; $skippedHere++; continue }
                    if ($path -match $gpuPattern -or [string]$r.category -match $gpuPattern) {
                        $counts.GpuSkipped++; $skippedHere++; continue
                    }
                    $category = Get-Category $path ([string]$r.category)
                    $table = $tableForCategory[$category]
                    if (-not $cache.ContainsKey($path)) {
                        Invoke-Db $connection @'
INSERT OR IGNORE INTO sensor_metadata
(sensor_path,sensor_name,category,unit,first_seen,last_seen)
VALUES (@path,@name,@category,@unit,@stamp,@stamp);
'@ @{path=$path;name=[string]$r.sensor_name;category=$category;unit=[string]$r.unit;stamp=$stamp} | Out-Null
                        $res = @(Invoke-Db $connection 'SELECT sensor_id FROM sensor_metadata WHERE sensor_path=@path;' @{path=$path})
                        if ($res.Count -eq 0) { throw "Sensor metadata lookup failed: $path" }
                        $cache[$path] = [long]$res[0].sensor_id
                    }
                    $sensorId = $cache[$path]
                    $exists = @(Invoke-Db $connection "SELECT 1 AS found FROM $table WHERE sensor_id=@sid AND timestamp=@stamp LIMIT 1;" @{sid=$sensorId;stamp=$stamp})
                    if ($exists.Count -gt 0) { $counts.Duplicate++; $skippedHere++; continue }
                    Invoke-Db $connection "INSERT INTO $table (sensor_id,timestamp,value,min_value,max_value,raw_value,raw_min,raw_max) VALUES (@sid,@stamp,@v,@mn,@mx,@rv,@rmn,@rmx);" @{
                        sid=$sensorId;stamp=$stamp
                        v=(To-NullableNumber ([string]$r.value)); mn=(To-NullableNumber ([string]$r.min_value)); mx=(To-NullableNumber ([string]$r.max_value))
                        rv=[string]$r.raw_value;rmn=[string]$r.raw_min;rmx=[string]$r.raw_max
                    } | Out-Null
                    # Only imported rows update metadata's last_seen.
                    Invoke-Db $connection 'UPDATE sensor_metadata SET sensor_name=@name, category=@category, unit=@unit, last_seen=CASE WHEN last_seen < @stamp THEN @stamp ELSE last_seen END WHERE sensor_id=@sid;' @{
                        name=[string]$r.sensor_name;category=$category;unit=[string]$r.unit;stamp=$stamp;sid=$sensorId
                    } | Out-Null
                } elseif ($file.Kind -eq 'Cycles') {
                    $table = 'monitor_cycles'
                    $exists = @(Invoke-Db $connection 'SELECT 1 AS found FROM monitor_cycles WHERE timestamp=@stamp AND sample_number=@num LIMIT 1;' @{stamp=$stamp;num=(To-NullableNumber ([string]$r.sample_number))})
                    if ($exists.Count -gt 0) { $counts.Duplicate++; $skippedHere++; continue }
                    $p = @{ stamp=$stamp; num=(To-NullableNumber ([string]$r.sample_number)); status=[string]$r.status
                        api=(To-NullableNumber ([string]$r.api_ms));sql=(To-NullableNumber ([string]$r.sqlite_ms));csv=(To-NullableNumber ([string]$r.csv_ms));total=(To-NullableNumber ([string]$r.total_ms))
                        detected=(To-NullableNumber ([string]$r.detected));ws=(To-NullableNumber ([string]$r.written_sqlite));wc=(To-NullableNumber ([string]$r.written_csv))
                        cpu=(To-NullableNumber ([string]$r.cpu));mem=(To-NullableNumber ([string]$r.memory));storage=(To-NullableNumber ([string]$r.storage))
                        mb=(To-NullableNumber ([string]$r.motherboard));network=(To-NullableNumber ([string]$r.network));battery=(To-NullableNumber ([string]$r.battery));other=(To-NullableNumber ([string]$r.other_sensors));err=[string]$r.error_message }
                    Invoke-Db $connection @'
INSERT INTO monitor_cycles
(timestamp,sample_number,status,api_ms,sqlite_ms,csv_ms,total_ms,detected,written_sqlite,written_csv,cpu,memory,storage,motherboard,network,battery,other_sensors,error_message)
VALUES (@stamp,@num,@status,@api,@sql,@csv,@total,@detected,@ws,@wc,@cpu,@mem,@storage,@mb,@network,@battery,@other,@err);
'@ $p | Out-Null
                } else {
                    $table = 'monitor_errors'
                    $p = @{stamp=$stamp;num=(To-NullableNumber ([string]$r.sample_number));stage=[string]$r.stage;msg=[string]$r.message;typ=[string]$r.exception_type}
                    $exists = @(Invoke-Db $connection 'SELECT 1 AS found FROM monitor_errors WHERE timestamp=@stamp AND sample_number=@num AND stage=@stage AND message=@msg LIMIT 1;' $p)
                    if ($exists.Count -gt 0) { $counts.Duplicate++; $skippedHere++; continue }
                    Invoke-Db $connection 'INSERT INTO monitor_errors (timestamp,sample_number,stage,message,exception_type) VALUES (@stamp,@num,@stage,@msg,@typ);' $p | Out-Null
                }
                $counts.Imported++
                $perTable[$table]++
                $fileInserted[$table]++
                $importedHere++
                if ($ShowEachRow) { Write-Step 'INSERT' "[$i/$($rows.Count)] $table | $stamp" 'Green' }
                } finally {
                    # A finally block runs even after a 'continue': progress includes duplicates/invalid/GPU rows.
                    if ($i -gt 0 -and (($i % $ProgressEvery -eq 0) -or ($i -eq $rows.Count))) {
                        $pct = if ($rows.Count -gt 0) { 100.0 * $i / $rows.Count } else { 100.0 }
                        $seconds = [Math]::Max(0.001,$fileWatch.Elapsed.TotalSeconds)
                        $rate = $i / $seconds
                        $remaining = if ($rate -gt 0) { [Math]::Max(0,($rows.Count-$i)/$rate) } else { 0 }
                        $summary = ('{0,6}/{1,-6} ({2,5:N1}%) | inserted={3}, duplicates={4}, GPU={5}, invalid={6} | {7:N1} rows/s | ETA {8:N1}s' -f `
                            $i,$rows.Count,$pct,$importedHere,($counts.Duplicate-$beforeDup),($counts.GpuSkipped-$beforeGpu),($counts.Invalid-$beforeInvalid),$rate,$remaining)
                        Write-Step 'PROGRESS' $summary 'Gray'
                        Write-Progress -Activity "Import $($file.Kind) CSV" -Status $summary -PercentComplete ([int][Math]::Min(100,$pct))
                    }
                }
            }
            Write-Progress -Activity "Import $($file.Kind) CSV" -Completed
            Invoke-Db $connection 'COMMIT;' | Out-Null
            $fileWatch.Stop()
            Write-Step 'COMMIT' "type=$($file.Kind) imported=$importedHere skipped=$skippedHere | elapsed=$([Math]::Round($fileWatch.Elapsed.TotalSeconds,2))s" 'Green'
            Write-Step 'FILE RESULT' "duplicates=$($counts.Duplicate-$beforeDup); gpu=$($counts.GpuSkipped-$beforeGpu); invalid=$($counts.Invalid-$beforeInvalid)" 'Cyan'
            foreach ($t in $measurementTables + @('monitor_cycles','monitor_errors')) {
                if ($fileInserted[$t] -gt 0) { Write-Step 'TABLE COUNT' ("{0,-17} +{1}" -f $t,$fileInserted[$t]) 'Green' }
            }
        } catch {
            try { Invoke-Db $connection 'ROLLBACK;' | Out-Null } catch { }
            throw "Import failed ($($file.Path), row $i). Transaction rolled back for this CSV: $($_.Exception.Message)"
        }
    }
    $watch.Stop()
    Write-Host ''
    Write-Host '================ IMPORT RESULT ================' -ForegroundColor Cyan
    Write-Step 'IMPORTED' $counts.Imported 'Green'
    Write-Step 'DUPLICATE' $counts.Duplicate 'Yellow'
    Write-Step 'GPU SKIP' $counts.GpuSkipped 'Yellow'
    Write-Step 'INVALID' $counts.Invalid 'Yellow'
    foreach ($table in $measurementTables + @('monitor_cycles','monitor_errors')) {
        Write-Step 'TABLE' ('{0,-17} +{1}' -f $table,$perTable[$table])
    }
    Write-Step 'ELAPSED' ('{0:n2} seconds' -f $watch.Elapsed.TotalSeconds) 'Cyan'
    Write-Step 'DATABASE' $DbPath 'Green'
    Write-Step 'LOG FILE' $logPath 'Green'
} finally {
    if ($null -ne $connection) { $connection.Dispose() }
}
