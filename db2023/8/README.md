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
