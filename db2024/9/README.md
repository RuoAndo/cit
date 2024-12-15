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

1. 相関サブクエリ
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
