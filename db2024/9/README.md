# データセット (12/15)
<pre>
1 employee
2 state_abberevs
3 state_areas
4 state_population
5 movie
6 slb_stock
7 Iris
8 California housing dataset
9 Prima Indians dataset
10 
11 
12 diabetes 
13 credit card fraud detection
</pre>

# SQL

1. 相関サブクエリ レンタル回数がちょうど20回の顧客
<pre>
sqlite> SELECT c.first_name, c.last_name FROM customer c WHERE 20 = (SELECT count(*) FROM rental r WHERE r.customer_id = c.customer_id) LIMIT 10;
LAUREN|HUDSON
JEANETTE|GREENE
TARA|RYAN
WILMA|RICHARDS
JO|FOWLER
KAY|CALDWELL
DANIEL|CABRAL
ANTHONY|SCHWAB
TERRY|GRISSOM
LUIS|YANEZ
</pre>

2. EXITSTS演算子 2005年5月25日よりも前に少なくも1本レンタルした顧客を列挙
<pre>
sqlite> SELECT c.first_name, c.last_name FROM customer c WHERE EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = c.customer_id AND date(r.rental_date) < '2005-05-25');
CHARLOTTE|HUNTER
DELORES|HANSEN
MINNIE|ROMERO
CASSANDRA|WALTERS
ANDREW|PURDY
MANUEL|MURRELL
TOMMY|COLLAZO
NELSON|CHRISTENSON
</pre>

3. 解析関数 各顧客の名前、住所、支払総額、レンタル回数のレポートを作成
payment, customer, address, cityの4つのテーブルを結合し、氏名に基づいてグループ化
<pre>
sqlite> SELECT c.first_name, c.last_name, ct.city, sum(p.amount) tot_payments, count(*) tot_rentals FROM payment p INNER JOIN customer c ON p.customer_id = c.customer_id INNER JOIN address a ON c.address_id = a.address_id INNER JOIN city ct ON a.city_id = ct.city_id GROUP BY c.first_name, c.last_name, ct.city LIMIT 10;
AARON|SELBY|Mwene-Ditu|110.76|24
ADAM|GOOCH|Adoni|101.78|22
ADRIAN|CLARY|Udine|74.81|19
AGNES|BISHOP|Sambhal|98.77|23
ALAN|KAHN|Emeishan|124.74|26
ALBERT|CROUSE|Bamenda|99.77|23
ALBERTO|HENNING|Barcelona|66.79|21
ALEX|GRESHAM|Uruapan|151.67|33
ALEXANDER|FENNELL|Bergamo|151.64|36
ALFRED|CASILLAS|Sawhaj|120.74|26
</pre>
