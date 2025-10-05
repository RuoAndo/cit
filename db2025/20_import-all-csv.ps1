# === 20_import-all-csv.ps1�i�C���ŁF�p�X�� / �ɕϊ��j ===
$Here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Db     = Join-Path $Here "mydata.db"
$sqlite = Join-Path $Here "sqlite3.exe"   # sqlite3.exe �̏ꏊ�ɍ��킹��

if (-not (Test-Path $Db)) {
    Write-Host "?? DB�V�K�쐬: $Db"
    New-Item -Path $Db -ItemType File | Out-Null
} else {
    Write-Host "?? ����DB�ɏ㏑��: $Db"
}

Get-ChildItem -Path $Here -Filter *.csv | ForEach-Object {
    if ($_.Length -eq 0) { Write-Warning "?? ��t�@�C��: $($_.Name)"; return }

    # �e�[�u�����̈��S��
    $name = $_.BaseName -replace '[^A-Za-z0-9_]', '_'
    if ($name -match '^[0-9]') { $name = "t_$name" }

    # �p�X�̋�؂�� / �ɕϊ��isqlite3 �Ɉ��S�ɓn���j
    $csvPath = ($_.FullName).Replace('\','/')

    Write-Host "?? ��荞�ݒ�: $($_.Name) �� [$name]"

    # 1) �e�[�u���폜
    & $sqlite $Db ("DROP TABLE IF EXISTS [{0}];" -f $name)

    # 2) �捞�i.mode �� .import �͕ʈ����ŏ������s�j
    & $sqlite $Db `
        ".mode csv" `
        (".import --csv --skip 1 ""{0}"" ""{1}""" -f $csvPath, $name)

    if ($LASTEXITCODE -eq 0) {
        Write-Host "? ����: $($_.Name) �� [$name]"
    } else {
        Write-Warning "? ���s: $($_.Name)"
    }
}

Write-Host "`n�m�F�R�}���h:"
Write-Host ".\sqlite3.exe `"$Db`""
Write-Host ".tables"
