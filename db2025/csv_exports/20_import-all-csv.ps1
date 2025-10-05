# === 20_import-all-csv.ps1（完全版：PowerShell構文修正版） ===
$Here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Db     = Join-Path $Here "mydata.db"
$sqlite = Join-Path $Here "sqlite3.exe"

if (-not (Test-Path $sqlite)) {
    Write-Error "sqlite3.exe が見つかりません: $sqlite"
    exit 1
}

if (-not (Test-Path $Db)) {
    Write-Host "?? DB新規作成: $Db"
    New-Item -Path $Db -ItemType File | Out-Null
} else {
    Write-Host "? 既存DBに上書き: $Db"
}

function Sanitize-Name([string]$name) {
    if ([string]::IsNullOrWhiteSpace($name)) { return "col" }
    $n = $name.Trim()
    $n = $n -replace '[^A-Za-z0-9_]', '_'
    if ($n -match '^[0-9]') { $n = "c_$n" }
    if ([string]::IsNullOrWhiteSpace($n) -or $n -eq '_') { $n = "col" }
    return $n
}

function Make-Unique([string[]]$cols) {
    $seen = @{}
    $out  = @()
    foreach ($c in $cols) {
        $base = $c
        $i = 1
        while ($seen.ContainsKey($c)) {
            $c = "${base}_$i"
            $i++
        }
        $seen[$c] = $true
        $out += $c
    }
    return ,$out
}

function Parse-Header([string]$rawHeader) {
    $hdr = @()
    $sb  = New-Object System.Text.StringBuilder
    $inQ = $false
    for ($i=0; $i -lt $rawHeader.Length; $i++) {
        $ch = $rawHeader[$i]
        if ($ch -eq '"') {
            if ($inQ -and $i+1 -lt $rawHeader.Length -and $rawHeader[$i+1] -eq '"') {
                $null = $sb.Append('"'); $i++
            } else {
                $inQ = -not $inQ
            }
        } elseif ($ch -eq ',' -and -not $inQ) {
            $hdr += $sb.ToString(); $sb.Clear() | Out-Null
        } else {
            $null = $sb.Append($ch)
        }
    }
    $hdr += $sb.ToString()
    return ,$hdr
}

function Invoke-Sqlite([string]$dbPath, [string]$sql) {
    & $sqlite $dbPath $sql
    return $LASTEXITCODE
}

Get-ChildItem -Path $Here -Filter *.csv | ForEach-Object {
    if ($_.Length -eq 0) { Write-Warning "? 空ファイル: $($_.Name)"; return }

    $name = $_.BaseName -replace '[^A-Za-z0-9_]', '_'
    if ($name -match '^[0-9]') { $name = "t_$name" }
    $stg  = "stg_$name"
    $csvPath = ($_.FullName).Replace('\','/')

    $rawHeader = (Get-Content -LiteralPath $_.FullName -TotalCount 1 -Encoding UTF8)
    if ([string]::IsNullOrWhiteSpace($rawHeader)) {
        Write-Warning "? ヘッダーが空: $($_.Name)"; return
    }
    if ($rawHeader[0] -eq [char]0xFEFF) { $rawHeader = $rawHeader.Substring(1) }

    $hdr  = Parse-Header $rawHeader
    $cols = $hdr | ForEach-Object { Sanitize-Name $_ }
    $cols = Make-Unique $cols
    if ($cols.Count -eq 0) { Write-Warning "? 列が検出できません: $($_.Name)"; return }

    Write-Host "?? 取り込み中: $($_.Name) → [$name]"
    Write-Host "   列: $($cols -join ', ')"

    # --- ステージングテーブル作成 ---
    $stgColsDef = ($cols | ForEach-Object { '"' + $_ + '" TEXT' }) -join ', '
    $sqlCreateStg = @"
DROP TABLE IF EXISTS "$stg";
CREATE TABLE "$stg" ($stgColsDef);
"@
    if ((Invoke-Sqlite $Db $sqlCreateStg) -ne 0) {
        Write-Warning "? ステージング作成失敗: $stg"
        return
    }

    # --- .import ---
    & $sqlite $Db `
        ".mode csv" `
        (".import --csv --skip 1 ""$csvPath"" ""$stg""")
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "? .import 失敗: $($_.Name)"
        return
    }

    # --- 型推定と主キー決定 ---
    $typedCols = @()
    $idCols    = @()
    foreach ($c in $cols) {
        $isInt = ($c -eq 'id' -or $c -match '.*_id$')
        if ($isInt) { $idCols += $c }
        if ($isInt) {
            $ctype = 'INTEGER'
        } else {
            $ctype = 'TEXT'
        }
        $typedCols += '"' + $c + '" ' + $ctype
    }

    $pkClause = ''
    if ($cols[0] -eq 'id') {
        $pkClause = 'PRIMARY KEY("id")'
    } else {
        $pkCandidates = $cols | Where-Object { $_ -match '.*_id$' }
        if ($pkCandidates.Count -ge 2) {
            $pkClause = 'PRIMARY KEY(' + (($pkCandidates | ForEach-Object { '"' + $_ + '"' }) -join ',') + ')'
        }
    }

    $allDefs = @($typedCols)
    if ($pkClause -ne '') { $allDefs += $pkClause }
    $createFinal = 'CREATE TABLE "' + $name + '" (' + ($allDefs -join ', ') + ');'

    $sqlCreateFinal = @"
DROP TABLE IF EXISTS "$name";
$createFinal
"@
    if ((Invoke-Sqlite $Db $sqlCreateFinal) -ne 0) {
        Write-Warning "? 本テーブル作成失敗: $name"
        return
    }

    # --- INSERT OR IGNORE ---
    $colList = ($cols | ForEach-Object { '"' + $_ + '"' }) -join ', '
    $sqlMove = @"
INSERT OR IGNORE INTO "$name" ($colList)
SELECT $colList FROM "$stg";
"@
    if ((Invoke-Sqlite $Db $sqlMove) -ne 0) {
        Write-Warning "? データ移送失敗: $name"
        return
    }

    # --- INDEX作成 ---
    $indexCmds = @()
    foreach ($c in $cols) {
        if ($c -match '.*_id$') {
            $idx = "${name}_${c}_idx"
            $indexCmds += "CREATE INDEX IF NOT EXISTS ""$idx"" ON ""$name""(""$c"");"
        }
    }
    if ($indexCmds.Count -gt 0) {
        $sqlIdx = [string]::Join("`n", $indexCmds)
        Invoke-Sqlite $Db $sqlIdx | Out-Null
    }

    Invoke-Sqlite $Db "DROP TABLE IF EXISTS ""$stg"";" | Out-Null
    Write-Host "? 完了: $($_.Name) → [$name]"
}

Write-Host "`n確認コマンド:"
Write-Host ".\sqlite3.exe `"$Db`""
Write-Host ".tables"
Write-Host "例: SELECT COUNT(*) FROM film_actor;"
