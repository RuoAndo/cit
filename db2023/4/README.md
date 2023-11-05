![image](https://github.com/RuoAndo/cit/assets/8035463/663f76b3-56c7-4a7c-8acb-7759e955576f)# 1. SELECTの実行時間を計測（シングルプロセス）
<img src="7-6.png">

# 2. 内部結合 (INNER JOIN)
<pre>
sqlite> SELECT first_name, last_name, address_id FROM customer LIMIT 5;
</pre>
<img src="customer.png">

<img src="address.png">
sqlite> SELECT first_name, last_name, address_id FROM customer LIMIT 5;

