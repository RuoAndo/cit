# === import-all-csv.ps1 ===
# �����f�B���N�g���̂��ׂĂ�CSV�� SQLite �Ɏ����C���|�[�g
# mydata.db �Ƃ���SQLite�f�[�^�x�[�X���쐬�i�����Ȃ�ǋL�j

$Db = ".\mydata.db"
$sqlite = "sqlite3.exe"

Get-ChildItem -Filter *.csv | ForEach-Object {
    $name = $_.BaseName -replace '[^A-Za-z0-9_]', '_'
    if ($name -match '^[0-9]') { $name = "t_$name" }

    & $sqlite $Db `
        "DROP TABLE IF EXISTS $name;" `
        ".mode csv" `
        ".import --csv --skip 1 '$($_.FullName)' $name"

    Write-Host "? $($_.Name) �� $name"
}
