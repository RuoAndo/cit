# ============================================================
# CPU Usage Report with SQLite VIEW
#
# 機能
# - SQLite DBへ接続
# - 必要なVIEWを作成
# - 概要レポート表示
# - CPU 80%以上を表示
# - 1分平均を表示
# - 1時間平均を表示
# - 最大CPU発生時刻を表示
# - CSVへ保存
# - 途中経過を表示
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=============================================="
Write-Host " CPU Usage Report - SQLite VIEW Version"
Write-Host "=============================================="
Write-Host ""

# ------------------------------------------------------------
# 設定
# ------------------------------------------------------------

$db = Join-Path $PSScriptRoot "02_cpu_usage.db"

$outputDir = Join-Path $PSScriptRoot "report"

$highCpuThreshold = 80


# ============================================================
# 1. PSSQLite
# ============================================================

Write-Host "[1/8] PSSQLiteを確認中..." -ForegroundColor Cyan

try {

    Import-Module PSSQLite -ErrorAction Stop

    Write-Host "[OK] PSSQLite読み込み完了" `
        -ForegroundColor Green
}
catch {

    Write-Host "[ERROR] PSSQLiteを読み込めません。" `
        -ForegroundColor Red

    Write-Host ""
    Write-Host "以下を実行してください。"
    Write-Host ""
    Write-Host "Install-Module PSSQLite -Scope CurrentUser"
    Write-Host ""

    exit 1
}

Write-Host ""


# ============================================================
# 2. DB確認
# ============================================================

Write-Host "[2/8] SQLite DBを確認中..." `
    -ForegroundColor Cyan

Write-Host "Database:"
Write-Host $db

if (-not (Test-Path $db)) {

    Write-Host ""
    Write-Host "[ERROR] DBファイルがありません。" `
        -ForegroundColor Red

    exit 1
}

Write-Host "[OK] DBファイル確認完了" `
    -ForegroundColor Green

Write-Host ""


# ============================================================
# 3. cpu_usage テーブル確認
# ============================================================

Write-Host "[3/8] cpu_usageテーブルを確認中..." `
    -ForegroundColor Cyan

$tableCheck = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT
    name
FROM
    sqlite_master
WHERE
    type = 'table'
    AND name = 'cpu_usage';
"@

if (-not $tableCheck) {

    Write-Host "[ERROR] cpu_usageテーブルがありません。" `
        -ForegroundColor Red

    exit 1
}

Write-Host "[OK] cpu_usageテーブル確認完了" `
    -ForegroundColor Green

Write-Host ""


# ============================================================
# 4. VIEW作成
# ============================================================

Write-Host "[4/8] レポート用VIEWを作成中..." `
    -ForegroundColor Cyan


# ------------------------------------------------------------
# VIEW 1
# 全体概要
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_summary"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_summary;

CREATE VIEW vw_cpu_summary AS

SELECT

    COUNT(*) AS samples,

    MIN(timestamp) AS start_time,

    MAX(timestamp) AS end_time,

    ROUND(
        AVG(cpu_percent),
        2
    ) AS avg_cpu,

    MAX(cpu_percent) AS max_cpu,

    MIN(cpu_percent) AS min_cpu,

    ROUND(
        AVG(user_percent),
        2
    ) AS avg_user,

    ROUND(
        AVG(privileged_percent),
        2
    ) AS avg_kernel,

    ROUND(
        AVG(idle_percent),
        2
    ) AS avg_idle,

    ROUND(
        AVG(interrupt_percent),
        2
    ) AS avg_interrupt,

    ROUND(
        AVG(current_clock_mhz),
        2
    ) AS avg_clock_mhz,

    MAX(current_clock_mhz)
        AS max_clock_mhz,

    MIN(current_clock_mhz)
        AS min_clock_mhz

FROM cpu_usage;
"@


# ------------------------------------------------------------
# VIEW 2
# CPU 80%以上
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_high"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_high;

CREATE VIEW vw_cpu_high AS

SELECT

    id,

    timestamp,

    cpu_percent,

    user_percent,

    privileged_percent,

    idle_percent,

    interrupt_percent,

    current_clock_mhz

FROM cpu_usage

WHERE
    cpu_percent >= $highCpuThreshold;
"@


# ------------------------------------------------------------
# VIEW 3
# 1分平均
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_minute"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_minute;

CREATE VIEW vw_cpu_minute AS

SELECT

    substr(
        timestamp,
        1,
        16
    ) AS minute,

    COUNT(*) AS samples,

    ROUND(
        AVG(cpu_percent),
        2
    ) AS avg_cpu,

    MAX(cpu_percent)
        AS max_cpu,

    MIN(cpu_percent)
        AS min_cpu,

    ROUND(
        AVG(user_percent),
        2
    ) AS avg_user,

    ROUND(
        AVG(privileged_percent),
        2
    ) AS avg_kernel,

    ROUND(
        AVG(idle_percent),
        2
    ) AS avg_idle,

    ROUND(
        AVG(interrupt_percent),
        2
    ) AS avg_interrupt,

    ROUND(
        AVG(current_clock_mhz),
        2
    ) AS avg_clock_mhz

FROM cpu_usage

GROUP BY

    substr(
        timestamp,
        1,
        16
    );
"@


# ------------------------------------------------------------
# VIEW 4
# 1時間平均
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_hour"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_hour;

CREATE VIEW vw_cpu_hour AS

SELECT

    substr(
        timestamp,
        1,
        13
    ) || ':00' AS hour,

    COUNT(*) AS samples,

    ROUND(
        AVG(cpu_percent),
        2
    ) AS avg_cpu,

    MAX(cpu_percent)
        AS max_cpu,

    MIN(cpu_percent)
        AS min_cpu,

    ROUND(
        AVG(user_percent),
        2
    ) AS avg_user,

    ROUND(
        AVG(privileged_percent),
        2
    ) AS avg_kernel,

    ROUND(
        AVG(idle_percent),
        2
    ) AS avg_idle,

    ROUND(
        AVG(interrupt_percent),
        2
    ) AS avg_interrupt,

    ROUND(
        AVG(current_clock_mhz),
        2
    ) AS avg_clock_mhz

FROM cpu_usage

GROUP BY

    substr(
        timestamp,
        1,
        13
    );
"@


# ------------------------------------------------------------
# VIEW 5
# 最大CPU値
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_peak"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_peak;

CREATE VIEW vw_cpu_peak AS

SELECT

    timestamp,

    cpu_percent,

    user_percent,

    privileged_percent,

    idle_percent,

    interrupt_percent,

    current_clock_mhz

FROM cpu_usage

WHERE
    cpu_percent =
    (
        SELECT
            MAX(cpu_percent)
        FROM cpu_usage
    );
"@


# ------------------------------------------------------------
# VIEW 6
# User / Kernel比率
# ------------------------------------------------------------

Write-Host "  -> vw_cpu_components"

Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
DROP VIEW IF EXISTS vw_cpu_components;

CREATE VIEW vw_cpu_components AS

SELECT

    timestamp,

    cpu_percent,

    user_percent,

    privileged_percent,

    idle_percent,

    ROUND(
        user_percent +
        privileged_percent,
        2
    ) AS user_plus_kernel,

    ROUND(
        cpu_percent -
        (
            user_percent +
            privileged_percent
        ),
        2
    ) AS difference

FROM cpu_usage;
"@

Write-Host ""
Write-Host "[OK] VIEW作成完了" `
    -ForegroundColor Green

Write-Host ""


# ============================================================
# 5. レポート取得
# ============================================================

Write-Host "[5/8] VIEWからレポート取得中..." `
    -ForegroundColor Cyan


$summary = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT *
FROM vw_cpu_summary;
"@


$high = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT *
FROM vw_cpu_high
ORDER BY timestamp;
"@


$minute = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT *
FROM vw_cpu_minute
ORDER BY minute;
"@


$hour = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT *
FROM vw_cpu_hour
ORDER BY hour;
"@


$peak = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT *
FROM vw_cpu_peak
ORDER BY timestamp;
"@


Write-Host "[OK] レポート取得完了" `
    -ForegroundColor Green

Write-Host ""


# ============================================================
# 6. 画面表示
# ============================================================

Write-Host "[6/8] レポートを表示します。" `
    -ForegroundColor Cyan

Write-Host ""

Write-Host "=============================================="
Write-Host " CPU SUMMARY"
Write-Host "=============================================="

Write-Host ""

Write-Host "測定件数"
Write-Host "  $($summary.samples)"

Write-Host ""

Write-Host "測定開始"
Write-Host "  $($summary.start_time)"

Write-Host ""

Write-Host "測定終了"
Write-Host "  $($summary.end_time)"

Write-Host ""

Write-Host "CPU"
Write-Host "  平均 : $($summary.avg_cpu) %"
Write-Host "  最大 : $($summary.max_cpu) %"
Write-Host "  最小 : $($summary.min_cpu) %"

Write-Host ""

Write-Host "User"
Write-Host "  平均 : $($summary.avg_user) %"

Write-Host ""

Write-Host "Kernel"
Write-Host "  平均 : $($summary.avg_kernel) %"

Write-Host ""

Write-Host "Idle"
Write-Host "  平均 : $($summary.avg_idle) %"

Write-Host ""

Write-Host "Interrupt"
Write-Host "  平均 : $($summary.avg_interrupt) %"

Write-Host ""

Write-Host "Clock"
Write-Host "  平均 : $($summary.avg_clock_mhz) MHz"
Write-Host "  最大 : $($summary.max_clock_mhz) MHz"
Write-Host "  最小 : $($summary.min_clock_mhz) MHz"


# ------------------------------------------------------------
# 高負荷
# ------------------------------------------------------------

Write-Host ""
Write-Host "=============================================="
Write-Host " HIGH CPU"
Write-Host " CPU >= $highCpuThreshold %"
Write-Host "=============================================="
Write-Host ""

if ($high) {

    Write-Host "件数: $(@($high).Count)"
    Write-Host ""

    $high |
        Format-Table `
            timestamp,
            cpu_percent,
            user_percent,
            privileged_percent,
            idle_percent,
            current_clock_mhz `
            -AutoSize
}
else {

    Write-Host "該当データなし"
}


# ------------------------------------------------------------
# CPU最大
# ------------------------------------------------------------

Write-Host ""
Write-Host "=============================================="
Write-Host " CPU PEAK"
Write-Host "=============================================="
Write-Host ""

$peak |
    Format-Table `
        timestamp,
        cpu_percent,
        user_percent,
        privileged_percent,
        idle_percent,
        current_clock_mhz `
        -AutoSize


# ------------------------------------------------------------
# 1分平均
# ------------------------------------------------------------

Write-Host ""
Write-Host "=============================================="
Write-Host " MINUTE REPORT"
Write-Host "=============================================="
Write-Host ""

$minute |
    Format-Table `
        minute,
        samples,
        avg_cpu,
        max_cpu,
        avg_user,
        avg_kernel,
        avg_idle `
        -AutoSize


# ------------------------------------------------------------
# 1時間平均
# ------------------------------------------------------------

Write-Host ""
Write-Host "=============================================="
Write-Host " HOURLY REPORT"
Write-Host "=============================================="
Write-Host ""

$hour |
    Format-Table `
        hour,
        samples,
        avg_cpu,
        max_cpu,
        avg_user,
        avg_kernel,
        avg_idle `
        -AutoSize


# ============================================================
# 7. CSV保存
# ============================================================

Write-Host ""
Write-Host "[7/8] CSVレポートを保存中..." `
    -ForegroundColor Cyan


if (-not (Test-Path $outputDir)) {

    New-Item `
        -ItemType Directory `
        -Path $outputDir |
        Out-Null

    Write-Host "reportフォルダを作成しました。"
}


$summaryFile =
    Join-Path $outputDir "cpu_summary.csv"

$highFile =
    Join-Path $outputDir "cpu_high.csv"

$minuteFile =
    Join-Path $outputDir "cpu_minute.csv"

$hourFile =
    Join-Path $outputDir "cpu_hour.csv"

$peakFile =
    Join-Path $outputDir "cpu_peak.csv"


$summary |
    Export-Csv `
        -Path $summaryFile `
        -NoTypeInformation `
        -Encoding UTF8


$high |
    Export-Csv `
        -Path $highFile `
        -NoTypeInformation `
        -Encoding UTF8


$minute |
    Export-Csv `
        -Path $minuteFile `
        -NoTypeInformation `
        -Encoding UTF8


$hour |
    Export-Csv `
        -Path $hourFile `
        -NoTypeInformation `
        -Encoding UTF8


$peak |
    Export-Csv `
        -Path $peakFile `
        -NoTypeInformation `
        -Encoding UTF8


Write-Host "[OK] CSV保存完了" `
    -ForegroundColor Green

Write-Host ""

Write-Host "保存先:"
Write-Host "  $outputDir"

Write-Host ""


# ============================================================
# 8. VIEW一覧
# ============================================================

Write-Host "[8/8] 作成済みVIEWを確認中..." `
    -ForegroundColor Cyan

$views = Invoke-SqliteQuery `
    -DataSource $db `
    -Query @"
SELECT
    name
FROM sqlite_master
WHERE
    type = 'view'
ORDER BY name;
"@

Write-Host ""

Write-Host "SQLite VIEW一覧"
Write-Host "--------------------------"

$views |
    Format-Table `
        name `
        -AutoSize


Write-Host ""
Write-Host "=============================================="
Write-Host " CPU Report 完了"
Write-Host "=============================================="
Write-Host ""