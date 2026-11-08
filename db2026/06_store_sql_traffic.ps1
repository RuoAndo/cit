
# ============================================================
# network_logs CSV -> SQLite
#
# PowerShell 5.1以降 / PSSQLite
#
# CSV検索先:
#   カレントディレクトリ\network_logs
#
# SQLite保存先:
#   カレントディレクトリ\network_monitor.db
#
# 対応ファイル:
#   adapter_traffic_*.csv
#   tcp_connections_*.csv
#   tcp_events_*.csv
#
# 機能:
# - CSVの一括検索・取り込み
# - SQLiteテーブル自動作成
# - INTEGER / REAL / TEXT 型変換
# - 既存データ保持
# - ファイル名＋行番号による重複防止
# - ファイル単位のトランザクション
# - 詳細ログ
# - 進行率と進捗バー
# - 処理速度
# - 推定残り時間
# - ファイル別集計
# - テーブル別集計
# - 全体の処理時間表示
# ============================================================

param(
    [ValidateRange(1, 1000000)]
    [int]$ProgressInterval = 100
)

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# 基本設定
# ------------------------------------------------------------

$startTime = Get-Date

$currentDir = (Get-Location).ProviderPath

$SourceDir = Join-Path $currentDir "network_logs"
$Database  = Join-Path $currentDir "network_monitor.db"

$connection = $null

$totalAdded     = 0
$totalDuplicate = 0
$totalInvalid   = 0

$successFiles = 0
$failedFiles  = 0
$skippedFiles = 0

$results = @()

# ------------------------------------------------------------
# 時間表示関数
# ------------------------------------------------------------

function Format-ElapsedTime {

    param(
        [TimeSpan]$Time
    )

    $days = [int][math]::Floor($Time.TotalDays)

    if ($days -gt 0) {
        return "{0}日 {1:00}:{2:00}:{3:00}" -f `
            $days,
            $Time.Hours,
            $Time.Minutes,
            $Time.Seconds
    }

    return "{0:00}:{1:00}:{2:00}" -f `
        [int]$Time.TotalHours,
        $Time.Minutes,
        $Time.Seconds
}

# ------------------------------------------------------------
# ログ出力関数
# ------------------------------------------------------------

function Write-Log {

    param(
        [string]$Message,
        [string]$Color = "White"
    )

    $timestamp = Get-Date -Format "HH:mm:ss"

    Write-Host "[$timestamp] $Message" `
        -ForegroundColor $Color
}

# ------------------------------------------------------------
# SQLite型変換
# ------------------------------------------------------------

function Convert-DbValue {

    param(
        [AllowNull()]$Value,
        [string]$Type
    )

    if ($null -eq $Value -or [string]$Value -eq "") {
        return [DBNull]::Value
    }

    switch ($Type) {

        "INTEGER" {
            return [long]::Parse(
                [string]$Value,
                [Globalization.CultureInfo]::InvariantCulture
            )
        }

        "REAL" {
            return [double]::Parse(
                [string]$Value,
                [Globalization.CultureInfo]::InvariantCulture
            )
        }

        default {
            return [string]$Value
        }
    }
}

# ------------------------------------------------------------
# テーブル定義
# ------------------------------------------------------------

$schemas = [ordered]@{

    adapter_traffic = [ordered]@{
        Timestamp      = "TEXT"
        Session        = "TEXT"
        Adapter        = "TEXT"
        RxBytes        = "INTEGER"
        TxBytes        = "INTEGER"
        RxKBps         = "REAL"
        TxKBps         = "REAL"
        ElapsedSeconds = "REAL"
    }

    tcp_connections = [ordered]@{
        Timestamp     = "TEXT"
        Session       = "TEXT"
        FirstSeen     = "TEXT"
        LocalAddress  = "TEXT"
        LocalPort     = "INTEGER"
        RemoteAddress = "TEXT"
        RemotePort    = "INTEGER"
        State         = "TEXT"
        PID           = "INTEGER"
        Process       = "TEXT"
        ProcessPath   = "TEXT"
        RemoteHost    = "TEXT"
    }

    tcp_events = [ordered]@{
        Timestamp     = "TEXT"
        Session       = "TEXT"
        Event         = "TEXT"
        FirstSeen     = "TEXT"
        LocalAddress  = "TEXT"
        LocalPort     = "INTEGER"
        RemoteAddress = "TEXT"
        RemotePort    = "INTEGER"
        State         = "TEXT"
        PreviousState = "TEXT"
        PID           = "INTEGER"
        Process       = "TEXT"
        ProcessPath   = "TEXT"
        RemoteHost    = "TEXT"
    }
}

# ------------------------------------------------------------
# メイン処理
# ------------------------------------------------------------

try {

    Write-Host ""
    Write-Host "========================================"
    Write-Host " Network CSV -> SQLite Import"
    Write-Host "========================================"

    Write-Log "処理開始" "Cyan"
    Write-Log "開始時刻: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))"
    Write-Log "カレントディレクトリ: $currentDir"
    Write-Log "CSV検索先: $SourceDir"
    Write-Log "SQLite保存先: $Database"
    Write-Log "進捗表示間隔: $ProgressInterval 行"

    # --------------------------------------------------------
    # PSSQLiteモジュール
    # --------------------------------------------------------

    Write-Log "PSSQLiteモジュール確認中..." "Cyan"

    Import-Module PSSQLite -ErrorAction Stop

    Write-Log "PSSQLite読み込み成功" "Green"

    # --------------------------------------------------------
    # CSVフォルダ確認
    # --------------------------------------------------------

    if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
        throw "CSVフォルダが存在しません: $SourceDir"
    }

    Write-Log "CSVフォルダ確認成功" "Green"

    # --------------------------------------------------------
    # CSV検索
    # --------------------------------------------------------

    Write-Log "CSVファイル検索開始..." "Cyan"

    $allFiles = @(
        Get-ChildItem `
            -LiteralPath $SourceDir `
            -Filter "*.csv" `
            -File |
            Sort-Object Name
    )

    $targetFiles = @(
        $allFiles | Where-Object {
            $_.Name -like "adapter_traffic_*.csv" -or
            $_.Name -like "tcp_connections_*.csv" -or
            $_.Name -like "tcp_events_*.csv"
        }
    )

    Write-Log "CSV総数: $($allFiles.Count)"
    Write-Log "取り込み対象: $($targetFiles.Count)" "Green"

    foreach ($file in $targetFiles) {
        Write-Log "検出: $($file.Name)"
    }

    if ($targetFiles.Count -eq 0) {
        Write-Log "対象CSVがありません。" "Yellow"
        return
    }

    # --------------------------------------------------------
    # SQLite接続
    # --------------------------------------------------------

    Write-Log "SQLite接続開始..." "Cyan"

    $connection = New-SQLiteConnection -DataSource $Database

    if ($null -eq $connection) {
        throw "SQLite接続オブジェクトを取得できません。"
    }

    Write-Log "SQLite接続成功" "Green"

    # --------------------------------------------------------
    # テーブル作成
    # --------------------------------------------------------

    foreach ($table in $schemas.Keys) {

        Write-Log "テーブル準備中: $table" "Cyan"

        $schema = $schemas[$table]

        $definitions = @(
            '"id" INTEGER PRIMARY KEY AUTOINCREMENT'
        )

        foreach ($name in $schema.Keys) {
            $definitions += ('"{0}" {1}' -f $name, $schema[$name])
        }

        $definitions += '"source_file" TEXT NOT NULL'
        $definitions += '"source_row" INTEGER NOT NULL'
        $definitions += 'UNIQUE("source_file", "source_row")'

        $createSQL = 'CREATE TABLE IF NOT EXISTS "{0}" ({1});' -f `
            $table, ($definitions -join ", ")

        $cmd = $connection.CreateCommand()

        try {

            $cmd.CommandText = $createSQL
            [void]$cmd.ExecuteNonQuery()

            foreach ($column in @("Timestamp", "Session")) {

                $indexSQL = `
                    'CREATE INDEX IF NOT EXISTS "idx_{0}_{1}" ON "{0}" ("{1}");' `
                    -f $table, $column

                $cmd.CommandText = $indexSQL

                [void]$cmd.ExecuteNonQuery()
            }

            # 既存テーブルの構造確認
            $cmd.CommandText = 'PRAGMA table_info("{0}");' -f $table

            $reader = $cmd.ExecuteReader()
            $existingColumns = @()

            try {
                while ($reader.Read()) {
                    $existingColumns += [string]$reader["name"]
                }
            }
            finally {
                $reader.Close()
                $reader.Dispose()
            }

            $requiredColumns = @($schema.Keys) +
                @("source_file", "source_row")

            $missingColumns = @(
                $requiredColumns | Where-Object {
                    $_ -notin $existingColumns
                }
            )

            if ($missingColumns.Count -gt 0) {
                throw (
                    "既存テーブル $table に列が不足しています: " +
                    ($missingColumns -join ", ")
                )
            }

            # 重複防止用のユニークインデックス
            $cmd.CommandText = @"
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_${table}_source"
ON "$table" ("source_file", "source_row");
"@

            [void]$cmd.ExecuteNonQuery()

        }
        finally {
            $cmd.Dispose()
        }

        Write-Log "テーブル準備完了: $table" "Green"
    }

    # --------------------------------------------------------
    # CSV取り込み
    # --------------------------------------------------------

    $fileIndex = 0

    foreach ($table in $schemas.Keys) {

        $schema = $schemas[$table]
        $columns = @($schema.Keys)

        $allColumns = @($columns) +
            @("source_file", "source_row")

        $quotedColumns = (
            $allColumns | ForEach-Object {
                '"{0}"' -f $_
            }
        ) -join ", "

        $placeholders = (
            $allColumns | ForEach-Object {
                '@{0}' -f $_
            }
        ) -join ", "

        $insertSQL = `
            'INSERT OR IGNORE INTO "{0}" ({1}) VALUES ({2});' `
            -f $table, $quotedColumns, $placeholders

        $pattern = "{0}_*.csv" -f $table

        $files = @(
            $targetFiles | Where-Object {
                $_.Name -like $pattern
            }
        )

        foreach ($file in $files) {

            $fileIndex++
            $fileStart = Get-Date

            Write-Host ""
            Write-Host "========================================"
            Write-Log "ファイル $fileIndex / $($targetFiles.Count)" "Cyan"
            Write-Log "ファイル名: $($file.Name)"
            Write-Log "テーブル: $table"
            Write-Log "サイズ: $($file.Length) bytes"
            Write-Log "開始: $($fileStart.ToString('HH:mm:ss'))"
            Write-Host "========================================"

            $tx = $null
            $cmd = $null
            $added = 0
            $duplicate = 0
            $invalid = 0
            $processed = 0

            try {

                # --------------------------------------------
                # CSV読み込み
                # --------------------------------------------

                Write-Log "CSV読み込み中..." "Cyan"

                $rows = @(
                    Import-Csv `
                        -LiteralPath $file.FullName `
                        -Encoding UTF8
                )

                $totalRows = $rows.Count

                Write-Log "読み込み完了: $totalRows 行" "Green"

                if ($totalRows -eq 0) {
                    Write-Log "空CSVのためスキップ" "Yellow"
                    $skippedFiles++
                    continue
                }

                # --------------------------------------------
                # ヘッダー検証
                # --------------------------------------------

                $headers = @(
                    $rows[0].PSObject.Properties.Name
                )

                $missing = @(
                    $columns | Where-Object {
                        $_ -notin $headers
                    }
                )

                if ($missing.Count -gt 0) {
                    throw "CSV列不足: $($missing -join ', ')"
                }

                Write-Log "CSVヘッダー検証成功" "Green"

                # --------------------------------------------
                # トランザクション開始
                # --------------------------------------------

                Write-Log "トランザクション開始"

                $tx = $connection.BeginTransaction()

                $cmd = $connection.CreateCommand()
                $cmd.Transaction = $tx
                $cmd.CommandText = $insertSQL

                foreach ($name in $allColumns) {
                    [void]$cmd.Parameters.AddWithValue(
                        "@$name",
                        [DBNull]::Value
                    )
                }

                $rowNo = 1

                Write-Log "SQLite登録開始..." "Cyan"

                # --------------------------------------------
                # 行単位の登録
                # --------------------------------------------

                foreach ($row in $rows) {

                    $rowNo++
                    $processed++

                    try {

                        foreach ($name in $columns) {

                            $value = Convert-DbValue `
                                -Value $row.$name `
                                -Type $schema[$name]

                            $cmd.Parameters["@$name"].Value = $value
                        }

                        $cmd.Parameters["@source_file"].Value = $file.Name
                        $cmd.Parameters["@source_row"].Value = $rowNo

                        $affected = $cmd.ExecuteNonQuery()

                        if ($affected -gt 0) {
                            $added++
                        }
                        else {
                            $duplicate++
                        }
                    }
                    catch {
                        $invalid++

                        Write-Log (
                            "行 {0}: エラー - {1}" -f `
                            $rowNo, $_.Exception.Message
                        ) "Red"
                    }

                    # ----------------------------------------
                    # 途中経過表示
                    # ----------------------------------------

                    if (
                        ($processed % $ProgressInterval -eq 0) -or
                        ($processed -eq $totalRows)
                    ) {

                        $percent = [math]::Round(
                            100.0 * $processed / $totalRows,
                            1
                        )

                        $elapsed = (Get-Date) - $fileStart

                        $seconds = [math]::Max(
                            0.001,
                            $elapsed.TotalSeconds
                        )

                        $speed = [math]::Round(
                            $processed / $seconds,
                            1
                        )

                        $remaining = $totalRows - $processed

                        $etaSeconds = $remaining /
                            [math]::Max(0.001, $speed)

                        $eta = [TimeSpan]::FromSeconds(
                            $etaSeconds
                        )

                        Write-Progress `
                            -Activity "SQLite: $($file.Name)" `
                            -Status "$processed / $totalRows 行 ($percent%)" `
                            -PercentComplete $percent

                        $message = (
                            "進捗: {0}/{1} ({2}%) | " +
                            "追加:{3} 重複:{4} 不正:{5} | " +
                            "速度:{6}行/秒 | " +
                            "経過:{7} | 残り:{8}"
                        ) -f `
                            $processed,
                            $totalRows,
                            $percent,
                            $added,
                            $duplicate,
                            $invalid,
                            $speed,
                            (Format-ElapsedTime $elapsed),
                            (Format-ElapsedTime $eta)

                        Write-Log $message "Cyan"
                    }
                }

                # --------------------------------------------
                # トランザクション確定
                # --------------------------------------------

                Write-Log "コミット開始..."

                $tx.Commit()

                Write-Log "コミット成功" "Green"

                $totalAdded += $added
                $totalDuplicate += $duplicate
                $totalInvalid += $invalid

                $successFiles++

                $fileElapsed = (Get-Date) - $fileStart

                $results += [PSCustomObject]@{
                    File      = $file.Name
                    Table     = $table
                    Rows      = $totalRows
                    Added     = $added
                    Duplicate = $duplicate
                    Invalid   = $invalid
                    Status    = "Success"
                    Seconds   = [math]::Round(
                        $fileElapsed.TotalSeconds, 2
                    )
                }

                Write-Host ""
                Write-Log "ファイル処理完了" "Green"
                Write-Log "追加: $added 件" "Green"
                Write-Log "重複: $duplicate 件"
                Write-Log "不正: $invalid 件"
                Write-Log "経過時間: $(Format-ElapsedTime $fileElapsed)"
                Write-Log "累積追加件数: $totalAdded"

            }
            catch {

                if ($null -ne $tx) {
                    try {
                        $tx.Rollback()
                    }
                    catch {
                        Write-Log "ロールバック失敗: $_" "Red"
                    }
                }

                $failedFiles++

                $fileElapsed = (Get-Date) - $fileStart

                $results += [PSCustomObject]@{
                    File      = $file.Name
                    Table     = $table
                    Rows      = $processed
                    Added     = 0
                    Duplicate = 0
                    Invalid   = $invalid
                    Status    = "Failed"
                    Seconds   = [math]::Round(
                        $fileElapsed.TotalSeconds, 2
                    )
                }

                Write-Log (
                    "ファイル処理失敗: {0}" -f `
                    $_.Exception.Message
                ) "Red"
            }
            finally {

                Write-Progress `
                    -Activity "SQLite: $($file.Name)" `
                    -Completed

                if ($null -ne $cmd) {
                    $cmd.Dispose()
                }

                if ($null -ne $tx) {
                    $tx.Dispose()
                }
            }
        }
    }

    # --------------------------------------------------------
    # ファイル別処理結果
    # --------------------------------------------------------

    Write-Host ""
    Write-Host "========================================"
    Write-Host " ファイル別処理結果"
    Write-Host "========================================"

    if ($results.Count -gt 0) {
        $results |
            Format-Table `
                File, Table, Rows, Added,
                Duplicate, Invalid, Status, Seconds `
                -AutoSize |
            Out-Host
    }

    # --------------------------------------------------------
    # テーブル別件数
    # --------------------------------------------------------

    Write-Host ""
    Write-Host "========================================"
    Write-Host " テーブル別データ件数"
    Write-Host "========================================"

    foreach ($table in $schemas.Keys) {

        $cmd = $connection.CreateCommand()

        try {

            $cmd.CommandText = `
                'SELECT COUNT(*) FROM "{0}";' -f $table

            $count = $cmd.ExecuteScalar()

            Write-Log "${table}: $count 件" "Green"
        }
        finally {
            $cmd.Dispose()
        }
    }

    # --------------------------------------------------------
    # 最終集計
    # --------------------------------------------------------

    $endTime = Get-Date
    $totalElapsed = $endTime - $startTime

    Write-Host ""
    Write-Host "========================================"
    Write-Host " 最終処理結果"
    Write-Host "========================================"

    Write-Log "開始時刻: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))"
    Write-Log "終了時刻: $($endTime.ToString('yyyy-MM-dd HH:mm:ss'))"

    Write-Log "対象CSV数: $($targetFiles.Count)"
    Write-Log "成功ファイル: $successFiles" "Green"
    Write-Log "失敗ファイル: $failedFiles"
    Write-Log "スキップ: $skippedFiles"

    Write-Log "追加レコード: $totalAdded" "Green"
    Write-Log "重複レコード: $totalDuplicate"
    Write-Log "不正レコード: $totalInvalid"

    Write-Log "総処理時間: $(Format-ElapsedTime $totalElapsed)" "Cyan"
    Write-Log "SQLite保存先: $Database" "Cyan"

    Write-Host "========================================"

    if ($failedFiles -eq 0 -and $totalInvalid -eq 0) {
        Write-Log "処理正常終了" "Green"
    }
    else {
        Write-Log "一部エラーがあります。" "Yellow"
    }

}
catch {

    Write-Log (
        "致命的エラー: {0}" -f $_.Exception.Message
    ) "Red"

}
finally {

    if ($null -ne $connection) {
        $connection.Dispose()
    }
}
