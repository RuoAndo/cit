# 1. Boost Spiript::X3でSQL文をparseする
<pre>
# g++ x3-sql-parser.cpp -std=c++17 -lboost_system
</pre>
<img src="x3.png">
<pre>
# ./a.out 
fields chr
fields pos
fields chrom
from variants
where chr=3 AND chr=4 
region exonic
</pre>


# 2. Eventテーブルを作成
<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023\8> python .\08_createEventTable.py
INSERTED: 0
INSERTED: 100
INSERTED: 200
INSERTED: 300
INSERTED: 400
INSERTED: 500
INSERTED: 600
INSERTED: 700
INSERTED: 800
INSERTED: 900
('2023-12-10 14:51:06', 19, 13, 'doraemon', 94)
('2023-12-10 11:54:29', 62, 14, 'bikkuriko', 22)
('2023-12-10 15:03:24', 35, 2, 'begita', 23)
('2023-12-09 09:46:48', 47, 2, 'doraemon', 91)
('2023-12-09 10:13:20', 9, 16, 'doraemon', 42)
('2023-12-10 08:17:57', 90, 25, 'doraemon', 57)
('2023-12-13 15:42:12', 85, 15, 'doraemon', 89)
('2023-12-09 09:13:49', 45, 3, 'doraemon', 75)
('2023-12-13 11:07:19', 33, 17, 'doraemon', 9)
('2023-12-11 13:51:29', 91, 13, 'doraemon', 2)
</pre>
2023-12-12に発生したイベントを見る
<pre>
sqlite> select * from event where date(ts) == '2023-12-12' LIMIT 5;
2023-12-12 08:24:50|68|20|doraemon|45
2023-12-12 14:05:38|50|23|doraemon|93
2023-12-12 10:56:05|13|10|bikkuriko|68
2023-12-12 15:23:02|12|18|doraemon|8
2023-12-12 10:40:16|81|4|doraemon|90
</pre>
イベントを多く生成しているplayer_idを検索
<pre>
sqlite> select player_id, count(*) from event where date(ts) == '2023-12-12' group by player_id ORDER BY count(*) DESC LIMIT 5;
24|12
6|12
29|11
5|11
16|10
</pre>
