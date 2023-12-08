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

#2. Eventテーブルを作成
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
('2023-12-11 12:39:10', 0, 16, 'begita', 53, 26, 68)
('2023-12-10 11:30:18', 1, 14, 'doraemon', 38, 39, 77)
('2023-12-12 09:20:36', 2, 13, 'doraemon', 19, 45, 34)
('2023-12-10 11:15:46', 3, 29, 'doraemon', 33, 26, 14)
('2023-12-12 10:15:47', 4, 17, 'doraemon', 79, 37, 38)
('2023-12-10 15:01:02', 5, 6, 'doraemon', 12, 75, 19)
('2023-12-09 11:56:11', 6, 14, 'doraemon', 13, 74, 41)
('2023-12-12 10:43:24', 7, 14, 'doraemon', 96, 94, 67)
('2023-12-13 15:04:45', 8, 10, 'doraemon', 55, 27, 21)
('2023-12-10 11:02:04', 9, 18, 'doraemon', 97, 99, 11)
</pre>
