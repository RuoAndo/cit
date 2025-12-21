$sqlite = ".\sqlite3.exe"
$dbPath = "game_3nf.db"

# 古いDBは消して作り直す
if (Test-Path $dbPath) { Remove-Item $dbPath }

# sqlite3 に .read させる（ここで PowerShell から日本語を流さないのがポイント）
& $sqlite $dbPath ".read create_tables_3nf.sql"
