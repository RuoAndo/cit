$sqlite = ".\sqlite3.exe"
$dbPath = "game_2nf.db"

# 古いDBは消して作り直す
if (Test-Path $dbPath) { Remove-Item $dbPath }

# sqlite3 に .read させる（ここで PowerShell から日本語を流さないのがポイント）
& $sqlite $dbPath ".read create_tables_2nf.sql"
