# === 20_import-all-csv.ps1�i���S�ŁFPowerShell�\���C���Łj ===
$Here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Db     = Join-Path $Here "mydata.db"
$sqlite = Join-Path $Here "sqlite3.exe"

if (-not (Test-Path $sqlite)) {
    Write-Error "sqlite3.exe ��������܂���: $sqlite"
    exit 1
}

if (-not (Test-Path $Db)) {
    Write-Host "?? DB�V�K�쐬: $Db"
    New-Item -Path $Db -ItemType File | Out-Null
} else {
    Write-Host "? ����DB�ɏ㏑��: $Db"
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
    if ($_.Length -eq 0) { Write-Warning "? ��t�@�C��: $($_.Name)"; return }

    $name = $_.BaseName -replace '[^A-Za-z0-9_]', '_'
    if ($name -match '^[0-9]') { $name = "t_$name" }
    $stg  = "stg_$name"
    $csvPath = ($_.FullName).Replace('\','/')

    $rawHeader = (Get-Content -LiteralPath $_.FullName -TotalCount 1 -Encoding UTF8)
    if ([string]::IsNullOrWhiteSpace($rawHeader)) {
        Write-Warning "? �w�b�_�[����: $($_.Name)"; return
    }
    if ($rawHeader[0] -eq [char]0xFEFF) { $rawHeader = $rawHeader.Substring(1) }

    $hdr  = Parse-Header $rawHeader
    $cols = $hdr | ForEach-Object { Sanitize-Name $_ }
    $cols = Make-Unique $cols
    if ($cols.Count -eq 0) { Write-Warning "? �񂪌��o�ł��܂���: $($_.Name)"; return }

    Write-Host "?? ��荞�ݒ�: $($_.Name) �� [$name]"
    Write-Host "   ��: $($cols -join ', ')"

    # --- �X�e�[�W���O�e�[�u���쐬 ---
    $stgColsDef = ($cols | ForEach-Object { '"' + $_ + '" TEXT' }) -join ', '
    $sqlCreateStg = @"
DROP TABLE IF EXISTS "$stg";
CREATE TABLE "$stg" ($stgColsDef);
"@
    if ((Invoke-Sqlite $Db $sqlCreateStg) -ne 0) {
        Write-Warning "? �X�e�[�W���O�쐬���s: $stg"
        return
    }

    # --- .import ---
    & $sqlite $Db `
        ".mode csv" `
        (".import --csv --skip 1 ""$csvPath"" ""$stg""")
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "? .import ���s: $($_.Name)"
        return
    }

    # --- �^����Ǝ�L�[���� ---
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
        Write-Warning "? �{�e�[�u���쐬���s: $name"
        return
    }

    # --- INSERT OR IGNORE ---
    $colList = ($cols | ForEach-Object { '"' + $_ + '"' }) -join ', '
    $sqlMove = @"
INSERT OR IGNORE INTO "$name" ($colList)
SELECT $colList FROM "$stg";
"@
    if ((Invoke-Sqlite $Db $sqlMove) -ne 0) {
        Write-Warning "? �f�[�^�ڑ����s: $name"
        return
    }

    # --- INDEX�쐬 ---
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
    Write-Host "? ����: $($_.Name) �� [$name]"
}

Write-Host "`n�m�F�R�}���h:"
Write-Host ".\sqlite3.exe `"$Db`""
Write-Host ".tables"
Write-Host "��: SELECT COUNT(*) FROM film_actor;"
