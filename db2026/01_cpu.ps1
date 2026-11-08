Import-Module PSSQLite

$db = "./01_cpu_usage.db"

# ÉeÅ[ÉuÉãçÏê¨
$query = @"
CREATE TABLE IF NOT EXISTS cpu_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_percent REAL NOT NULL
);
"@

Invoke-SqliteQuery -DataSource $db -Query $query

while ($true) {

    $cpu = Get-CimInstance Win32_Processor |
        Measure-Object -Property LoadPercentage -Average |
        Select-Object -ExpandProperty Average

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    $insert = @"
INSERT INTO cpu_usage (
    timestamp,
    cpu_percent
)
VALUES (
    '$timestamp',
    $cpu
);
"@

    Invoke-SqliteQuery -DataSource $db -Query $insert

    Write-Host "$timestamp CPU: $cpu %"

    Start-Sleep -Seconds 1
}