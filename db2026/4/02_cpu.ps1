# ============================================================
# CPU情報を1秒ごとに取得してSQLiteへ保存
# 既存DBの不足列を自動追加
# 処理途中の進捗を詳細表示
# ============================================================

Write-Host ""
Write-Host "========================================"
Write-Host " CPU Monitor + SQLite Logger"
Write-Host "========================================"
Write-Host ""

# ------------------------------------------------------------
# 1. PSSQLite読み込み
# ------------------------------------------------------------

Write-Host "[1/5] PSSQLiteを読み込み中..." -ForegroundColor Cyan

try {

    Import-Module PSSQLite -ErrorAction Stop

    Write-Host "[OK] PSSQLite読み込み完了" `
        -ForegroundColor Green
}
catch {

    Write-Host "[ERROR] PSSQLiteを読み込めません。" `
        -ForegroundColor Red

    Write-Host $_.Exception.Message `
        -ForegroundColor Red

    exit
}

Write-Host ""

# ------------------------------------------------------------
# 2. DB確認
# ------------------------------------------------------------

Write-Host "[2/5] データベースを確認中..." `
    -ForegroundColor Cyan

$db = Join-Path $PSScriptRoot "02_cpu_usage.db"

Write-Host "Database: $db"

$createTable = @"
CREATE TABLE IF NOT EXISTS cpu_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_percent REAL
);
"@

try {

    Invoke-SqliteQuery `
        -DataSource $db `
        -Query $createTable `
        -ErrorAction Stop

    Write-Host "[OK] cpu_usage テーブル確認完了" `
        -ForegroundColor Green
}
catch {

    Write-Host "[ERROR] テーブル作成・確認失敗" `
        -ForegroundColor Red

    Write-Host $_.Exception.Message

    exit
}

Write-Host ""

# ------------------------------------------------------------
# 3. 列確認
# ------------------------------------------------------------

Write-Host "[3/5] 必要な列を確認中..." `
    -ForegroundColor Cyan

$requiredColumns = [ordered]@{

    "user_percent"            = "REAL"

    "privileged_percent"      = "REAL"

    "idle_percent"            = "REAL"

    "interrupt_percent"       = "REAL"

    "current_clock_mhz"       = "INTEGER"

    "max_clock_mhz"           = "INTEGER"

    "core_count"              = "INTEGER"

    "logical_processor_count" = "INTEGER"

    "cpu_name"                = "TEXT"
}

$currentColumns = Invoke-SqliteQuery `
    -DataSource $db `
    -Query "PRAGMA table_info(cpu_usage);"

$currentColumnNames = @(
    $currentColumns |
    ForEach-Object {
        $_.name
    }
)

foreach ($column in $requiredColumns.Keys) {

    if ($currentColumnNames -contains $column) {

        Write-Host "[OK] $column は存在します" `
            -ForegroundColor DarkGreen
    }
    else {

        $type = $requiredColumns[$column]

        Write-Host "[追加] $column ($type)" `
            -ForegroundColor Yellow

        $alter = @"
ALTER TABLE cpu_usage
ADD COLUMN $column $type;
"@

        try {

            Invoke-SqliteQuery `
                -DataSource $db `
                -Query $alter `
                -ErrorAction Stop

            Write-Host "      -> 追加完了" `
                -ForegroundColor Green
        }
        catch {

            Write-Host "      -> 追加失敗" `
                -ForegroundColor Red

            Write-Host $_.Exception.Message
        }
    }
}

Write-Host ""
Write-Host "[OK] DB構造確認完了" `
    -ForegroundColor Green

Write-Host ""

# ------------------------------------------------------------
# CPU情報表示
# ------------------------------------------------------------

Write-Host "[4/5] CPU監視を開始します。" `
    -ForegroundColor Cyan

Write-Host ""
Write-Host "Ctrl + C で終了できます。"
Write-Host ""

$counter = 0

# ------------------------------------------------------------
# 4. 監視ループ
# ------------------------------------------------------------

while ($true) {

    $counter++

    Write-Host "----------------------------------------"

    Write-Host "測定回数: $counter" `
        -ForegroundColor Magenta

    try {

        # ----------------------------------------------------
        # CPU基本情報取得
        # ----------------------------------------------------

        Write-Host "CPU基本情報を取得中..." `
            -ForegroundColor DarkGray

        $cpuInfo = Get-CimInstance `
            Win32_Processor |
            Select-Object -First 1

        Write-Host "[OK] CPU基本情報取得完了" `
            -ForegroundColor Green

        # ----------------------------------------------------
        # CPU性能情報取得
        # ----------------------------------------------------

        Write-Host "CPUパフォーマンス情報を取得中..." `
            -ForegroundColor DarkGray

        $perf = Get-CimInstance `
            Win32_PerfFormattedData_PerfOS_Processor |
            Where-Object {
                $_.Name -eq "_Total"
            } |
            Select-Object -First 1

        Write-Host "[OK] CPUパフォーマンス取得完了" `
            -ForegroundColor Green

        # ----------------------------------------------------
        # 時刻
        # ----------------------------------------------------

        $timestamp =
            Get-Date -Format "yyyy-MM-dd HH:mm:ss"

        # ----------------------------------------------------
        # 値取得
        # ----------------------------------------------------

        $cpuPercent =
            [double]$perf.PercentProcessorTime

        $userPercent =
            [double]$perf.PercentUserTime

        $privilegedPercent =
            [double]$perf.PercentPrivilegedTime

        $idlePercent =
            [double]$perf.PercentIdleTime

        $interruptPercent =
            [double]$perf.PercentInterruptTime

        $currentClock =
            [int]$cpuInfo.CurrentClockSpeed

        $maxClock =
            [int]$cpuInfo.MaxClockSpeed

        $coreCount =
            [int]$cpuInfo.NumberOfCores

        $logicalCount =
            [int]$cpuInfo.NumberOfLogicalProcessors

        $cpuName =
            [string]$cpuInfo.Name

        $cpuNameSql =
            $cpuName.Replace("'", "''")

        # ----------------------------------------------------
        # 取得値表示
        # ----------------------------------------------------

        Write-Host ""

        Write-Host "取得値:" `
            -ForegroundColor Cyan

        Write-Host "  Timestamp : $timestamp"

        Write-Host "  CPU       : $cpuPercent %"

        Write-Host "  User      : $userPercent %"

        Write-Host "  Kernel    : $privilegedPercent %"

        Write-Host "  Idle      : $idlePercent %"

        Write-Host "  Interrupt : $interruptPercent %"

        Write-Host "  Clock     : $currentClock MHz"

        Write-Host "  MaxClock  : $maxClock MHz"

        Write-Host "  Core      : $coreCount"

        Write-Host "  Logical   : $logicalCount"

        Write-Host "  CPU Name  : $cpuName"

        Write-Host ""

        # ----------------------------------------------------
        # SQLite保存
        # ----------------------------------------------------

        Write-Host "SQLiteへ保存中..." `
            -ForegroundColor DarkGray

        $insert = @"
INSERT INTO cpu_usage (
    timestamp,
    cpu_percent,
    user_percent,
    privileged_percent,
    idle_percent,
    interrupt_percent,
    current_clock_mhz,
    max_clock_mhz,
    core_count,
    logical_processor_count,
    cpu_name
)
VALUES (
    '$timestamp',
    $cpuPercent,
    $userPercent,
    $privilegedPercent,
    $idlePercent,
    $interruptPercent,
    $currentClock,
    $maxClock,
    $coreCount,
    $logicalCount,
    '$cpuNameSql'
);
"@

        Invoke-SqliteQuery `
            -DataSource $db `
            -Query $insert `
            -ErrorAction Stop

        Write-Host "[OK] SQLite保存完了" `
            -ForegroundColor Green

        # ----------------------------------------------------
        # 保存件数確認
        # ----------------------------------------------------

        $countResult = Invoke-SqliteQuery `
            -DataSource $db `
            -Query "SELECT COUNT(*) AS count FROM cpu_usage;"

        $recordCount =
            $countResult.count

        Write-Host "現在の保存件数: $recordCount 件" `
            -ForegroundColor Cyan

        # ----------------------------------------------------
        # 1行要約
        # ----------------------------------------------------

        Write-Host ""

        Write-Host (
            "{0} | CPU:{1}% | User:{2}% | Kernel:{3}% | Idle:{4}% | Clock:{5}MHz" `
                -f `
                $timestamp,
                $cpuPercent,
                $userPercent,
                $privilegedPercent,
                $idlePercent,
                $currentClock
        ) -ForegroundColor White
    }
    catch {

        Write-Host ""
        Write-Host "[ERROR] 処理中にエラーが発生しました。" `
            -ForegroundColor Red

        Write-Host $_.Exception.Message `
            -ForegroundColor Red
    }

    # --------------------------------------------------------
    # 5. 待機
    # --------------------------------------------------------

    Write-Host ""
    Write-Host "[5/5] 次の測定まで1秒待機..." `
        -ForegroundColor DarkGray

    Start-Sleep -Seconds 1
}