# === 20_import-all-csv.ps1（修正版：パスを / に変換） ===
$Here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Db     = Join-Path $Here "mydata.db"
$sqlite = Join-Path $Here "sqlite3.exe"   # sqlite3.exe の場所に合わせて

if (-not (Test-Path $Db)) {
    Write-Host "?? DB新規作成: $Db"
    New-Item -Path $Db -ItemType File | Out-Null
} else {
    Write-Host "?? 既存DBに上書き: $Db"
}

Get-ChildItem -Path $Here -Filter *.csv | ForEach-Object {
    if ($_.Length -eq 0) { Write-Warning "?? 空ファイル: $($_.Name)"; return }

    # テーブル名の安全化
    $name = $_.BaseName -replace '[^A-Za-z0-9_]', '_'
    if ($name -match '^[0-9]') { $name = "t_$name" }

    # パスの区切りを / に変換（sqlite3 に安全に渡す）
    $csvPath = ($_.FullName).Replace('\','/')

    Write-Host "?? 取り込み中: $($_.Name) → [$name]"

    # 1) テーブル削除
    & $sqlite $Db ("DROP TABLE IF EXISTS [{0}];" -f $name)

    # 2) 取込（.mode と .import は別引数で順次実行）
    & $sqlite $Db `
        ".mode csv" `
        (".import --csv --skip 1 ""{0}"" ""{1}""" -f $csvPath, $name)

    if ($LASTEXITCODE -eq 0) {
        Write-Host "? 完了: $($_.Name) → [$name]"
    } else {
        Write-Warning "? 失敗: $($_.Name)"
    }
}

Write-Host "`n確認コマンド:"
Write-Host ".\sqlite3.exe `"$Db`""
Write-Host ".tables"
