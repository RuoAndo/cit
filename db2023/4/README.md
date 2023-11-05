# 1. SELECTの実行時間を計測（シングルプロセス）
<img src="7-6.png">
<img src="plot11.png" width=70%>

# 2. 内部結合 (INNER JOIN)
<pre>
sqlite> SELECT first_name, last_name, address_id FROM customer LIMIT 5;
</pre>
<img src="customer.png">

<pre>
sqlite> SELECT first_name, last_name, address_id FROM customer LIMIT 5;
</pre>
<img src="address.png">
<pre>
JOIN  
sqlite> SELECT C.first_name, C.last_name, A.address FROM customer C JOIN address A ON A.address_id = C.address_id LIMIT 5;
</pre>
<img src="join1.png">

# 3. csvファイルのインポートとエクスポート
<pre>
sqlite> .mode csv
sqlite> .import ./BostonHousing.csv boston
sqlite> .headers on
sqlite> .mode csv
sqlite> .once exporttest.csv
sqlite> select crim,zn,indus,chas,nox,rm,age,dis from boston;
sqlite>
(base) PS C:\Users\flare\OneDrive\cit\db2023\4> more .\exporttest.csv
crim,zn,indus,chas,nox,rm,age,dis
0.00632,18,2.31,0,0.538,6.575,65.2,4.09
0.02731,0,7.07,0,0.469,6.421,78.9,4.9671
</pre>
