
#requires -Version 5.1
<#
.SYNOPSIS
 TCP connections, network adapter byte rates,
 and optional SQLite collection.

.DESCRIPTION
 CSV output works without external modules.
 If -SQLite is specified, requires PSSQLite:
 Install-Module PSSQLite -Scope CurrentUser

 Packet payloads are not captured.
 Use pktmon separately.

.EXAMPLE
 .\Monitor-Network-Full.ps1 -IntervalSeconds 1

.EXAMPLE
 .\Monitor-Network-Full.ps1 -SQLite -AllStates -IntervalSeconds 2

.EXAMPLE
 .\Monitor-Network-Full.ps1 -DurationMinutes 10 -ResolveDNS
#>

[CmdletBinding()]
param(
    [ValidateRange(1,3600)]
    [int]$IntervalSeconds = 1,

    [ValidateRange(1,1000)]
    [int]$ShowTop = 25,

    [switch]$AllStates,
    [switch]$ResolveDNS,
    [switch]$SQLite,

    [ValidateRange(0,1000000)]
    [int]$DurationMinutes = 0,

    [string]$OutputDir = (
        Join-Path (Get-Location).Path 'network_logs'
    )
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ==================================================
# 1. 保存先とファイル名
# ==================================================

$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)

New-Item -ItemType Directory `
    -Path $OutputDir -Force | Out-Null

$session = Get-Date -Format 'yyyyMMdd-HHmmss'

$connectionsCsv = Join-Path $OutputDir `
    "tcp_connections_$session.csv"

$eventsCsv = Join-Path $OutputDir `
    "tcp_events_$session.csv"

$trafficCsv = Join-Path $OutputDir `
    "adapter_traffic_$session.csv"

$dbFile = Join-Path $OutputDir 'network_monitor.sqlite'

$connectionColumns = @(
    'Timestamp','Session','FirstSeen',
    'LocalAddress','LocalPort',
    'RemoteAddress','RemotePort',
    'State','PID','Process',
    'ProcessPath','RemoteHost'
)

$eventColumns = @(
    'Timestamp','Session','Event','FirstSeen',
    'LocalAddress','LocalPort',
    'RemoteAddress','RemotePort',
    'State','PreviousState','PID',
    'Process','ProcessPath','RemoteHost'
)

$trafficColumns = @(
    'Timestamp','Session','Adapter',
    'RxBytes','TxBytes',
    'RxKBps','TxKBps','ElapsedSeconds'
)

# ==================================================
# 2. CSV出力関数
# ==================================================

function Initialize-CsvFile {
    param(
        [string]$Path,
        [string[]]$Columns
    )

    $header = (
        $Columns | ForEach-Object {
            '"' + ($_ -replace '"','""') + '"'
        }
    ) -join ','

    [System.IO.File]::WriteAllText(
        $Path,
        $header + [Environment]::NewLine,
        (New-Object System.Text.UTF8Encoding($true))
    )
}

function Add-CsvRows {
    param(
        [string]$Path,
        [object[]]$Rows
    )

    if ($null -ne $Rows -and $Rows.Count -gt 0) {
        $Rows | Export-Csv `
            -LiteralPath $Path `
            -NoTypeInformation `
            -Append `
            -Encoding UTF8
    }
}

# ==================================================
# 3. SQLite出力関数
# ==================================================

function Escape-SqlText {
    param(
        [AllowNull()][object]$Value
    )

    if ($null -eq $Value) {
        return 'NULL'
    }

    return "'" + (
        [string]$Value
    ).Replace("'", "''") + "'"
}

function Write-SqlRows {
    param(
        [string]$TableName,
        [string[]]$ColumnNames,
        [object[]]$Rows
    )

    if (
        -not $SQLite -or
        $null -eq $Rows -or
        $Rows.Count -eq 0
    ) {
        return
    }

    $statements = New-Object `
        'System.Collections.Generic.List[string]'

    $statements.Add('BEGIN TRANSACTION;')

    $cols = (
        $ColumnNames | ForEach-Object {
            '"' + $_ + '"'
        }
    ) -join ','

    foreach ($row in $Rows) {
        $vals = (
            $ColumnNames | ForEach-Object {
                Escape-SqlText $row.$_
            }
        ) -join ','

        $statements.Add(
            "INSERT INTO $TableName ($cols) VALUES ($vals);"
        )
    }

    $statements.Add('COMMIT;')

    Invoke-SqliteQuery `
        -DataSource $dbFile `
        -Query ($statements -join "`n") |
        Out-Null
}

# ==================================================
# 4. プロセス情報取得
# ==================================================

function Get-ProcessRecord {
    param([int]$TargetPID)

    try {
        $p = Get-Process -Id $TargetPID `
            -ErrorAction Stop

        $exe = ''

        try {
            $exe = [string]$p.Path
        } catch {
        }

        return [pscustomobject]@{
            Name = [string]$p.ProcessName
            Path = $exe
        }
    } catch {
        return [pscustomobject]@{
            Name = ''
            Path = ''
        }
    }
}

# ==================================================
# 5. 逆引きDNS
# ==================================================

function Get-CachedDns {
    param([string]$Address)

    if (
        -not $ResolveDNS -or
        [string]::IsNullOrWhiteSpace($Address)
    ) {
        return ''
    }

    if ($script:dnsCache.ContainsKey($Address)) {
        return $script:dnsCache[$Address]
    }

    $hostname = ''

    try {
        $hostname = (
            [System.Net.Dns]::GetHostEntry($Address)
        ).HostName
    } catch {
    }

    $script:dnsCache[$Address] = $hostname

    return $hostname
}

# ==================================================
# 6. CSV初期化
# ==================================================

Initialize-CsvFile `
    -Path $connectionsCsv `
    -Columns $connectionColumns

Initialize-CsvFile `
    -Path $eventsCsv `
    -Columns $eventColumns

Initialize-CsvFile `
    -Path $trafficCsv `
    -Columns $trafficColumns

# ==================================================
# 7. SQLite初期化
# ==================================================

if ($SQLite) {

    if (-not (Get-Module -ListAvailable -Name PSSQLite)) {
        throw @'
PSSQLite が見つかりません。
Install-Module PSSQLite -Scope CurrentUser
を実行するか、-SQLite を外してください。
'@
    }

    Import-Module PSSQLite -ErrorAction Stop

    $create = @'
CREATE TABLE IF NOT EXISTS tcp_connections (
 Timestamp TEXT,
 Session TEXT,
 FirstSeen TEXT,
 LocalAddress TEXT,
 LocalPort INTEGER,
 RemoteAddress TEXT,
 RemotePort INTEGER,
 State TEXT,
 PID INTEGER,
 Process TEXT,
 ProcessPath TEXT,
 RemoteHost TEXT
);

CREATE TABLE IF NOT EXISTS tcp_events (
 Timestamp TEXT,
 Session TEXT,
 Event TEXT,
 FirstSeen TEXT,
 LocalAddress TEXT,
 LocalPort INTEGER,
 RemoteAddress TEXT,
 RemotePort INTEGER,
 State TEXT,
 PreviousState TEXT,
 PID INTEGER,
 Process TEXT,
 ProcessPath TEXT,
 RemoteHost TEXT
);

CREATE TABLE IF NOT EXISTS adapter_traffic (
 Timestamp TEXT,
 Session TEXT,
 Adapter TEXT,
 RxBytes TEXT,
 TxBytes TEXT,
 RxKBps REAL,
 TxKBps REAL,
 ElapsedSeconds REAL
);

CREATE INDEX IF NOT EXISTS idx_tcp_time
ON tcp_connections(Timestamp);

CREATE INDEX IF NOT EXISTS idx_tcp_remote
ON tcp_connections(RemoteAddress);

CREATE INDEX IF NOT EXISTS idx_events_time
ON tcp_events(Timestamp);

CREATE INDEX IF NOT EXISTS idx_traffic_time
ON adapter_traffic(Timestamp);
'@

    Invoke-SqliteQuery `
        -DataSource $dbFile `
        -Query $create | Out-Null
}

# ==================================================
# 8. 監視準備
# ==================================================

$previous = @{}
$previousTraffic = @{}
$dnsCache = @{}

$started = Get-Date
$poll = 0

Write-Host "監視開始: $($started.ToString('yyyy-MM-dd HH:mm:ss'))" `
    -ForegroundColor Cyan

Write-Host "保存先: $OutputDir"
Write-Host ('SQLite: ' + [bool]$SQLite)
Write-Host ('DNS逆引き: ' + [bool]$ResolveDNS)
Write-Host 'Ctrl+C で停止します。'

# ==================================================
# 9. メイン監視ループ
# ==================================================

try {
    while ($true) {

        $loopStart = Get-Date

        if (
            $DurationMinutes -gt 0 -and
            ($loopStart - $started).TotalMinutes -ge $DurationMinutes
        ) {
            break
        }

        $timestamp = $loopStart.ToString(
            'yyyy-MM-dd HH:mm:ss.fff'
        )

        $current = @{}

        $connections = New-Object System.Collections.ArrayList
        $events = New-Object System.Collections.ArrayList
        $traffic = New-Object System.Collections.ArrayList

        $procCache = @{}

        # ------------------------------------------
        # TCP接続取得
        # ------------------------------------------

        try {
            $tcp = @(
                Get-NetTCPConnection -ErrorAction Stop
            )
        } catch {
            Write-Warning "TCP取得失敗: $($_.Exception.Message)"
            Start-Sleep -Seconds $IntervalSeconds
            continue
        }

        if (-not $AllStates) {
            $tcp = @(
                $tcp | Where-Object {
                    $_.State -eq 'Established'
                }
            )
        }

        foreach ($c in $tcp) {

            $ownerPid = [int]$c.OwningProcess

            if (-not $procCache.ContainsKey($ownerPid)) {
                $procCache[$ownerPid] = `
                    Get-ProcessRecord -TargetPID $ownerPid
            }

            $proc = $procCache[$ownerPid]

            $key = ('{0}|{1}|{2}|{3}|{4}' -f `
                $c.LocalAddress,
                $c.LocalPort,
                $c.RemoteAddress,
                $c.RemotePort,
                $ownerPid
            )

            $state = [string]$c.State
            $firstSeen = $timestamp
            $event = 'NEW'
            $previousState = ''

            if ($previous.ContainsKey($key)) {

                $firstSeen = [string]$previous[$key].FirstSeen
                $previousState = [string]$previous[$key].State

                if ($previousState -eq $state) {
                    $event = ''
                } else {
                    $event = 'STATE_CHANGED'
                }
            }

            $rec = [pscustomobject][ordered]@{
                Timestamp     = $timestamp
                Session       = $session
                FirstSeen     = $firstSeen
                LocalAddress  = [string]$c.LocalAddress
                LocalPort     = [int]$c.LocalPort
                RemoteAddress = [string]$c.RemoteAddress
                RemotePort    = [int]$c.RemotePort
                State         = $state
                PID           = $ownerPid
                Process       = $proc.Name
                ProcessPath   = $proc.Path
                RemoteHost    = (
                    Get-CachedDns -Address (
                        [string]$c.RemoteAddress
                    )
                )
            }

            $current[$key] = $rec

            [void]$connections.Add($rec)

            if ($event) {

                [void]$events.Add(
                    [pscustomobject][ordered]@{
                        Timestamp     = $timestamp
                        Session       = $session
                        Event         = $event
                        FirstSeen     = $firstSeen
                        LocalAddress  = $rec.LocalAddress
                        LocalPort     = $rec.LocalPort
                        RemoteAddress = $rec.RemoteAddress
                        RemotePort    = $rec.RemotePort
                        State         = $state
                        PreviousState = $previousState
                        PID           = $ownerPid
                        Process       = $proc.Name
                        ProcessPath   = $proc.Path
                        RemoteHost    = $rec.RemoteHost
                    }
                )
            }
        }

        # ------------------------------------------
        # 消失したTCP接続の検出
        # ------------------------------------------

        foreach ($key in $previous.Keys) {

            if (-not $current.ContainsKey($key)) {

                $old = $previous[$key]

                [void]$events.Add(
                    [pscustomobject][ordered]@{
                        Timestamp     = $timestamp
                        Session       = $session
                        Event         = 'DISAPPEARED'
                        FirstSeen     = $old.FirstSeen
                        LocalAddress  = $old.LocalAddress
                        LocalPort     = $old.LocalPort
                        RemoteAddress = $old.RemoteAddress
                        RemotePort    = $old.RemotePort
                        State         = ''
                        PreviousState = $old.State
                        PID           = $old.PID
                        Process       = $old.Process
                        ProcessPath   = $old.ProcessPath
                        RemoteHost    = $old.RemoteHost
                    }
                )
            }
        }

        # ------------------------------------------
        # ネットワーク送受信速度
        # ------------------------------------------

        try {

            $adapterStatistics = @(
                Get-NetAdapterStatistics -ErrorAction Stop
            )

            foreach ($s in $adapterStatistics) {

                $rxRate = 0.0
                $txRate = 0.0
                $elapsed = 0.0

                $rx = [double]$s.ReceivedBytes
                $tx = [double]$s.SentBytes

                if ($previousTraffic.ContainsKey($s.Name)) {

                    $old = $previousTraffic[$s.Name]

                    $elapsed = (
                        $loopStart - $old.Time
                    ).TotalSeconds

                    if ($elapsed -gt 0) {
                        $rxRate = [math]::Max(
                            0,
                            ($rx - $old.Rx) / $elapsed / 1024
                        )

                        $txRate = [math]::Max(
                            0,
                            ($tx - $old.Tx) / $elapsed / 1024
                        )
                    }
                }

                $previousTraffic[$s.Name] = @{
                    Rx   = $rx
                    Tx   = $tx
                    Time = $loopStart
                }

                [void]$traffic.Add(
                    [pscustomobject][ordered]@{
                        Timestamp      = $timestamp
                        Session        = $session
                        Adapter        = [string]$s.Name
                        RxBytes        = [string]$s.ReceivedBytes
                        TxBytes        = [string]$s.SentBytes
                        RxKBps         = [math]::Round($rxRate,2)
                        TxKBps         = [math]::Round($txRate,2)
                        ElapsedSeconds = [math]::Round($elapsed,3)
                    }
                )
            }

        } catch {
            Write-Warning "アダプター取得失敗: $($_.Exception.Message)"
        }

        # ------------------------------------------
        # CSVとSQLite保存
        # ------------------------------------------

        $connectionRows = @($connections.ToArray())
        $eventRows = @($events.ToArray())
        $trafficRows = @($traffic.ToArray())

        try {

            Add-CsvRows `
                -Path $connectionsCsv `
                -Rows $connectionRows

            Add-CsvRows `
                -Path $eventsCsv `
                -Rows $eventRows

            Add-CsvRows `
                -Path $trafficCsv `
                -Rows $trafficRows

            Write-SqlRows `
                -TableName 'tcp_connections' `
                -ColumnNames $connectionColumns `
                -Rows $connectionRows

            Write-SqlRows `
                -TableName 'tcp_events' `
                -ColumnNames $eventColumns `
                -Rows $eventRows

            Write-SqlRows `
                -TableName 'adapter_traffic' `
                -ColumnNames $trafficColumns `
                -Rows $trafficRows

        } catch {
            Write-Warning "保存失敗: $($_.Exception.Message)"
        }

        # ------------------------------------------
        # 前回の状態を更新
        # ------------------------------------------

        $previous = $current
        $poll++

        # ------------------------------------------
        # コンソール表示
        # ------------------------------------------

        Clear-Host

        Write-Host "=== TCP Network Monitor ===" `
            -ForegroundColor Cyan

        $newCount = @(
            $eventRows | Where-Object Event -eq 'NEW'
        ).Count

        $disappearedCount = @(
            $eventRows | Where-Object Event -eq 'DISAPPEARED'
        ).Count

        Write-Host (
            "時刻: $timestamp / サンプル: $poll / " +
            "TCP: $($connectionRows.Count) / " +
            "新規: $newCount / 消失: $disappearedCount"
        )

        Write-Host ""
        Write-Host '--- TCP接続 ---' `
            -ForegroundColor Yellow

        $connectionRows |
            Select-Object -First $ShowTop `
                LocalAddress,
                LocalPort,
                RemoteAddress,
                RemotePort,
                State,
                PID,
                Process |
            Format-Table -AutoSize |
            Out-Host

        Write-Host '--- アダプター速度 (KB/s) ---' `
            -ForegroundColor Yellow

        $trafficRows |
            Select-Object Adapter,RxKBps,TxKBps |
            Format-Table -AutoSize |
            Out-Host

        Write-Host "保存先: $OutputDir / Ctrl+C で終了"

        # ------------------------------------------
        # 監視間隔の調整
        # ------------------------------------------

        $nextSleep = $IntervalSeconds - (
            (Get-Date) - $loopStart
        ).TotalSeconds

        if ($nextSleep -gt 0) {
            Start-Sleep -Milliseconds (
                [int]($nextSleep * 1000)
            )
        }
    }

} finally {
    Write-Host "終了。ログ保存先: $OutputDir" `
        -ForegroundColor Cyan

    if ($SQLite) {
        Write-Host "SQLite DB: $dbFile"
    }
}
