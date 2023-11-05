# 1. SELECTの実行時間を計測（シングルプロセス）
<img src="7-6.png">
<img src="plot11.png">

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
