# テストデータ(JSON, CSV)の生成

dummyjson sample-json.hbs > test_data.json
dummyjson sample-csv.hbs > test_data.csv

# CSVファイルの取り込み

Use ".open FILENAME" to reopen on a persistent database.
sqlite> .mode csv

sqlite> .import test_data.csv test_data
test_data.csv:2: expected 8 columns but found 7 - filling the rest with NULL

sqlite> .tables
test_data

sqlite> select * from test_data where id=48;
48,"Francis Winter",Xenosys,1989,"65 Elton Way",Medford,false,
