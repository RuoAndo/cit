# 前回の続き
<pre>
(base) PS C:\Users\flare\OneDrive\cit\db2023\3> cp ..\2\sakila_master.db .
(base) PS C:\Users\flare\OneDrive\cit\db2023\3> .\sqlite3.exe .\sakila_master.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> .tables
actor                   film                    payment
address                 film_actor              rental
category                film_category           sales_by_film_category
city                    film_list               sales_by_store
country                 film_text               staff
customer                inventory               staff_list
customer_list           language                store
</pre>

# .helpでコマンド一覧を表示する

<pre>
sqlite> .help
.archive ...             Manage SQL archives
.auth ON|OFF             Show authorizer callbacks
.backup ?DB? FILE        Backup DB (default "main") to FILE
.bail on|off             Stop after hitting an error.  Default OFF
.binary on|off           Turn binary output on or off.  Default OFF
.cd DIRECTORY            Change the working directory to DIRECTORY
.changes on|off          Show number of rows changed by SQL
.check GLOB              Fail if output since .testcase does not match
.clone NEWDB             Clone data into NEWDB from the existing database
.connection [close] [#]  Open or close an auxiliary database connection
.databases               List names and files of attached databases
.dbconfig ?op? ?val?     List or change sqlite3_db_config() options
.dbinfo ?DB?             Show status information about the database
.dump ?OBJECTS?          Render database content as SQL
.echo on|off             Turn command echo on or off
.eqp on|off|full|...     Enable or disable automatic EXPLAIN QUERY PLAN
.excel                   Display the output of next command in spreadsheet
.exit ?CODE?             Exit this program with return-code CODE
.expert                  EXPERIMENTAL. Suggest indexes for queries
.explain ?on|off|auto?   Change the EXPLAIN formatting mode.  Default: auto
.filectrl CMD ...        Run various sqlite3_file_control() operations
.fullschema ?--indent?   Show schema and the content of sqlite_stat tables
.headers on|off          Turn display of headers on or off
.help ?-all? ?PATTERN?   Show help text for PATTERN
.import FILE TABLE       Import data from FILE into TABLE
.imposter INDEX TABLE    Create imposter table TABLE on index INDEX
.indexes ?TABLE?         Show names of indexes
.limit ?LIMIT? ?VAL?     Display or change the value of an SQLITE_LIMIT
.lint OPTIONS            Report potential schema issues.
.load FILE ?ENTRY?       Load an extension library
.log FILE|off            Turn logging on or off.  FILE can be stderr/stdout
.mode MODE ?OPTIONS?     Set output mode
.nonce STRING            Suspend safe mode for one command if nonce matches
.nullvalue STRING        Use STRING in place of NULL values
.once ?OPTIONS? ?FILE?   Output for the next SQL command only to FILE
.open ?OPTIONS? ?FILE?   Close existing database and reopen FILE
.output ?FILE?           Send output to FILE or stdout if FILE is omitted
.parameter CMD ...       Manage SQL parameter bindings
.print STRING...         Print literal STRING
.progress N              Invoke progress handler after every N opcodes
.prompt MAIN CONTINUE    Replace the standard prompts
.quit                    Exit this program
.read FILE               Read input from FILE or command output
.recover                 Recover as much data as possible from corrupt db.
.restore ?DB? FILE       Restore content of DB (default "main") from FILE
.save ?OPTIONS? FILE     Write database to FILE (an alias for .backup ...)
.scanstats on|off        Turn sqlite3_stmt_scanstatus() metrics on or off
.schema ?PATTERN?        Show the CREATE statements matching PATTERN
.selftest ?OPTIONS?      Run tests defined in the SELFTEST table
.separator COL ?ROW?     Change the column and row separators
.session ?NAME? CMD ...  Create or control sessions
.sha3sum ...             Compute a SHA3 hash of database content
.shell CMD ARGS...       Run CMD ARGS... in a system shell
.show                    Show the current values for various settings
.stats ?ARG?             Show stats or turn stats on or off
.system CMD ARGS...      Run CMD ARGS... in a system shell
.tables ?TABLE?          List names of tables matching LIKE pattern TABLE
.testcase NAME           Begin redirecting output to 'testcase-out.txt'
.testctrl CMD ...        Run various sqlite3_test_control() operations
.timeout MS              Try opening locked tables for MS milliseconds
.timer on|off            Turn SQL timer on or off
.trace ?OPTIONS?         Output each SQL statement as it is run
.vfsinfo ?AUX?           Information about the top-level VFS
.vfslist                 List all available VFSes
.vfsname ?AUX?           Print the name of the VFS stack
.width NUM1 NUM2 ...     Set minimum column widths for columnar output
</pre>

# actorのスキーマを表示する

<pre>
sqlite> .schema actor
CREATE TABLE actor (
  actor_id numeric NOT NULL ,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (actor_id)
  );
CREATE INDEX idx_actor_last_name ON actor(last_name)
;
CREATE TRIGGER actor_trigger_ai AFTER INSERT ON actor
 BEGIN
  UPDATE actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
CREATE TRIGGER actor_trigger_au AFTER UPDATE ON actor
 BEGIN
  UPDATE actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
 </pre>

# customerの先頭10人を表示する

<pre>
sqlite> select first_name, last_name from customer limit 10;
MARY|SMITH
PATRICIA|JOHNSON
LINDA|WILLIAMS
BARBARA|JONES
ELIZABETH|BROWN
JENNIFER|DAVIS
MARIA|MILLER
SUSAN|WILSON
MARGARET|MOORE
DOROTHY|TAYLOR
</pre>

# customerのMARY SMITHのデータを表示する
sqlite> select * from customer where first_name="MARY" and last_name="SMITH";
1|1|MARY|SMITH|MARY.SMITH@sakilacustomer.org|5|1|2006-02-14 22:04:36.000|2020-12-23 07:15:11

# rentalのスキーマを表示する。

<pre>
sqlite> .schema rental
CREATE TABLE rental (
  rental_id INT NOT NULL,
  rental_date TIMESTAMP NOT NULL,
  inventory_id INT  NOT NULL,
  customer_id INT  NOT NULL,
  return_date TIMESTAMP DEFAULT NULL,
  staff_id SMALLINT  NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY (rental_id),
  CONSTRAINT fk_rental_staff FOREIGN KEY (staff_id) REFERENCES staff (staff_id) ,
  CONSTRAINT fk_rental_inventory FOREIGN KEY (inventory_id) REFERENCES inventory (inventory_id) ,
  CONSTRAINT fk_rental_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);
CREATE INDEX idx_rental_fk_inventory_id ON rental(inventory_id)
;
CREATE INDEX idx_rental_fk_customer_id ON rental(customer_id)
;
CREATE INDEX idx_rental_fk_staff_id ON rental(staff_id)
;
CREATE UNIQUE INDEX idx_rental_uq  ON rental (rental_date,inventory_id,customer_id)
;
CREATE TRIGGER rental_trigger_ai AFTER INSERT ON rental
 BEGIN
  UPDATE rental SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
CREATE TRIGGER rental_trigger_au AFTER UPDATE ON rental
 BEGIN
  UPDATE rental SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
</pre>

# id番号5のcustomerのレンタル状況を調べる

<pre>
sqlite> select * from rental where customer_id = 5 limit 10;
731|2005-05-29 07:25:16.000|4124|5|2005-05-30 05:21:16.000|1|2020-12-23 07:15:29
1085|2005-05-31 11:15:43.000|301|5|2005-06-07 12:02:43.000|1|2020-12-23 07:15:34
1142|2005-05-31 19:46:38.000|3998|5|2005-06-05 14:03:38.000|1|2020-12-23 07:15:35
1502|2005-06-15 22:03:14.000|3277|5|2005-06-23 18:42:14.000|2|2020-12-23 07:15:40
1631|2005-06-16 08:01:02.000|2466|5|2005-06-19 09:04:02.000|1|2020-12-23 07:15:41
2063|2005-06-17 15:56:53.000|4323|5|2005-06-21 14:19:53.000|1|2020-12-23 07:15:48
2570|2005-06-19 04:20:13.000|1105|5|2005-06-25 07:00:13.000|1|2020-12-23 07:15:55
3126|2005-06-20 18:38:22.000|1183|5|2005-06-26 00:00:22.000|1|2020-12-23 07:16:02
3677|2005-07-06 09:11:58.000|600|5|2005-07-08 10:50:58.000|2|2020-12-23 07:16:11
4889|2005-07-08 20:04:43.000|4463|5|2005-07-13 17:57:43.000|2|2020-12-23 07:16:29
</pre>

# 内部結合: customerとrentalのテーブルを結合し、customer_idのレンタル状況と名前を表示する。

<pre>
sqlite> SELECT customer.first_name, customer.last_name, rental.customer_id, rental.rental_date FROM rental INNER JOIN customer ON rental.customer_id = customer.customer_id where customer.customer_id = 10;
DOROTHY|TAYLOR|10|2005-05-31 19:36:30.000
DOROTHY|TAYLOR|10|2005-06-16 20:21:53.000
DOROTHY|TAYLOR|10|2005-06-17 11:11:14.000
DOROTHY|TAYLOR|10|2005-06-18 03:26:23.000
DOROTHY|TAYLOR|10|2005-06-19 20:01:59.000
DOROTHY|TAYLOR|10|2005-06-20 00:00:55.000
DOROTHY|TAYLOR|10|2005-07-06 14:13:45.000
DOROTHY|TAYLOR|10|2005-07-07 03:06:40.000
DOROTHY|TAYLOR|10|2005-07-07 14:14:13.000
DOROTHY|TAYLOR|10|2005-07-09 03:12:52.000
DOROTHY|TAYLOR|10|2005-07-09 04:53:18.000
DOROTHY|TAYLOR|10|2005-07-09 21:58:57.000
DOROTHY|TAYLOR|10|2005-07-10 20:41:09.000
DOROTHY|TAYLOR|10|2005-07-28 05:21:42.000
DOROTHY|TAYLOR|10|2005-07-28 15:10:55.000
DOROTHY|TAYLOR|10|2005-07-28 22:34:12.000
DOROTHY|TAYLOR|10|2005-07-31 15:27:07.000
DOROTHY|TAYLOR|10|2005-08-01 17:09:59.000
DOROTHY|TAYLOR|10|2005-08-02 14:55:00.000
DOROTHY|TAYLOR|10|2005-08-02 19:13:39.000
DOROTHY|TAYLOR|10|2005-08-17 20:11:35.000
DOROTHY|TAYLOR|10|2005-08-18 09:19:12.000
DOROTHY|TAYLOR|10|2005-08-19 19:23:30.000
DOROTHY|TAYLOR|10|2005-08-20 16:43:28.000
DOROTHY|TAYLOR|10|2005-08-22 21:59:29.000
</pre>


  
# csvファイルの読み込み
<pre>
sqlite> .mode csv
sqlite> .import ./BostonHousing.csv boston
sqlite> .schema boston
CREATE TABLE IF NOT EXISTS "boston"(
"crim" TEXT, "zn" TEXT, "indus" TEXT, "chas" TEXT,
 "nox" TEXT, "rm" TEXT, "age" TEXT, "dis" TEXT,
 "rad" TEXT, "tax" TEXT, "ptratio" TEXT, "b" TEXT,
 "lstat" TEXT, "medv" TEXT);
</pre>

#  Boston Housing データセットの項目の説明
<pre>
CRIM： 町別の「犯罪率」
ZN： 25,000平方フィートを超える区画に分類される住宅地の割合＝「広い家の割合」
INDUS： 町別の「非小売業の割合」
CHAS： チャールズ川のダミー変数（区画が川に接している場合は1、そうでない場合は0）＝「川の隣か」
NOX： 「NOx濃度（0.1ppm単位）」＝一酸化窒素濃度（parts per 10 million単位）。この項目を目的変数とする場合もある
RM： 1戸当たりの「平均部屋数」
AGE： 1940年より前に建てられた持ち家の割合＝「古い家の割合」
DIS： 5つあるボストン雇用センターまでの加重距離＝「主要施設への距離」
RAD： 「主要高速道路へのアクセス性」の指数
TAX： 10,000ドル当たりの「固定資産税率」
PTRATIO： 町別の「生徒と先生の比率」
B： 「1000(Bk - 0.63)」の二乗値。Bk＝「町ごとの黒人の割合」を指す
LSTAT： 「低所得者人口の割合」
MEDV：「住宅価格」（1000ドル単位）の中央値。通常はこの数値が目的変数として使われる
</pre>

# 課題 データベースから、PTRATIO： 町別の「生徒と先生の比率」の列を取り出しなさい。
