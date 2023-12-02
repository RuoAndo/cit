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
