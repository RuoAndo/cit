<pre>
PS D:\cit\db2025> cp ..\db2024\sqlite3.exe .
PS D:\cit\db2025> .\sqlite3.exe
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open cpu_log.db
sqlite> .tables
cpu_log
sqlite> .scheme cpu_log
Error: unknown command or invalid arguments:  "scheme". Enter ".help" for help
sqlite> .schema cpu_log
CREATE TABLE cpu_log (Timestamp TEXT, CPU_Total REAL, CPU_0 REAL, CPU_1 REAL, CPU_2 REAL, CPU_3 REAL, UserPct REAL, SystemPct REAL, IdlePct REAL, InterruptPct REAL, DpcPct REAL, CtxSwitches INTEGER, Interrupts INTEGER, SoftInterrupts INTEGER, Syscalls INTEGER, FreqCurrentMHz REAL);
</pre>