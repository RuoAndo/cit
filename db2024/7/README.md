# テーブル項目修正 (2024-12-01)
<img src="ER_7.jpeg">

# 7.1 playerテーブルとeventテーブルの結合
<pre>
sqlite> SELECT player.first_name, player.last_name, player.player_rank, event.* FROM event JOIN player ON event.player_id = player.player_id WHERE event.player_id = 20 LIMIT 5;
VLNJX|ckhKB|3|6|2024-12-04 12:09:59|7|20|20|8|28|recover
VLNJX|ckhKB|3|21|2024-12-04 10:47:04|1|20|53|1|19|recover
VLNJX|ckhKB|3|25|2024-12-05 10:33:37|87|20|33|19|3|attack
VLNJX|ckhKB|3|36|2024-12-04 11:49:38|76|20|5|19|19|attack
VLNJX|ckhKB|3|39|2024-12-02 10:08:17|97|20|44|2|21|attack
</pre>

# 7.2 sakila - テーブルの結合: 郵便番号で検索 (addressとcustomer)
<pre>
sqlite> SELECT c.first_name, c.last_name, a.address FROM customer c INNER JOIN address a ON c.address_id = a.address_id WHERE a.postal_code = 52137;
JAMES|GANNON|1635 Kuwana Boulevard
FREDDIE|DUGGAN|1103 Quilmes Boulevard
</pre>
<pre>
sqlite> .schema address
CREATE TABLE address (
  address_id int NOT NULL,
  address VARCHAR(50) NOT NULL,
  address2 VARCHAR(50) DEFAULT NULL,
  district VARCHAR(20) NOT NULL,
  city_id INT  NOT NULL,
  postal_code VARCHAR(10) DEFAULT NULL,
  phone VARCHAR(20) NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (address_id),
  CONSTRAINT fk_address_city FOREIGN KEY (city_id) REFERENCES city (city_id) ON DELETE NO ACTION ON UPDATE CASCADE
);

sqlite> .schema customer
CREATE TABLE customer (
  customer_id INT NOT NULL,
  store_id INT NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(50) DEFAULT NULL,
  address_id INT NOT NULL,
  active CHAR(1) DEFAULT 'Y' NOT NULL,
  create_date TIMESTAMP NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (customer_id),
  CONSTRAINT fk_customer_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT fk_customer_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE NO ACTION ON UPDATE CASCADE
);
</pre>

# 7.3 sakila - 3つ以上のテーブルを結合 (addressとcustomerとcity)
<pre>
sqlite> select c.first_name, c.last_name, ct.city FROM customer c INNER JOIN address a ON c.address_id = a.address_id INNER JOIN city ct ON a.city_id = ct.city_id LIMIT 5;
MARY|SMITH|Sasebo
PATRICIA|JOHNSON|San Bernardino
LINDA|WILLIAMS|Athenai
BARBARA|JONES|Myingyan
ELIZABETH|BROWN|Nantou
</pre>
<pre>
sqlite> .schema city
CREATE TABLE city (
  city_id int NOT NULL,
  city VARCHAR(50) NOT NULL,
  country_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (city_id),
  CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE NO ACTION ON UPDATE CASCADE
);
</pre>

# 7.4 player_id = 20 の名前と、期間内にどのような行動をとったか集計する (GROUP BY)
<pre>
sqlite> SELECT player.first_name, player.last_name, player.player_rank, event.*, count(*) FROM event JOIN player ON event.player_id = player.player_id WHERE event.player_id = 20 GROUP BY action_type;
VLNJX|ckhKB|3|250|2024-12-01 09:55:15|30|20|93|27|1|attack|2
VLNJX|ckhKB|3|703|2024-12-02 12:29:57|27|20|19|9|10|attack|1
VLNJX|ckhKB|3|276|2024-12-04 15:54:54|40|20|17|1|11|attack|1
VLNJX|ckhKB|3|376|2024-12-02 11:37:40|97|20|4|26|14|attack|1
VLNJX|ckhKB|3|176|2024-12-01 09:27:55|28|20|8|12|15|recover|2
VLNJX|ckhKB|3|517|2024-12-05 12:39:11|96|20|30|19|17|attack|1
VLNJX|ckhKB|3|355|2024-12-02 12:39:36|92|20|56|22|18|attack|3
VLNJX|ckhKB|3|21|2024-12-04 10:47:04|1|20|53|1|19|recover|3
VLNJX|ckhKB|3|883|2024-12-04 14:28:15|50|20|64|2|2|recover|1
VLNJX|ckhKB|3|793|2024-12-03 15:49:09|46|20|89|29|20|attack|1
VLNJX|ckhKB|3|39|2024-12-02 10:08:17|97|20|44|2|21|attack|1
VLNJX|ckhKB|3|779|2024-12-01 11:31:14|59|20|60|17|22|attack|1
VLNJX|ckhKB|3|409|2024-12-02 15:47:36|4|20|45|2|23|recover|1
VLNJX|ckhKB|3|610|2024-12-04 10:48:06|38|20|66|25|26|attack|2
VLNJX|ckhKB|3|160|2024-12-03 10:57:09|95|20|29|11|27|attack|2
VLNJX|ckhKB|3|6|2024-12-04 12:09:59|7|20|20|8|28|recover|4
VLNJX|ckhKB|3|82|2024-12-02 11:35:10|82|20|71|28|29|recover|1
VLNJX|ckhKB|3|25|2024-12-05 10:33:37|87|20|33|19|3|attack|1
VLNJX|ckhKB|3|366|2024-12-02 12:28:45|15|20|96|10|4|attack|1
VLNJX|ckhKB|3|267|2024-12-02 09:46:32|46|20|97|14|5|recover|1
VLNJX|ckhKB|3|122|2024-12-04 15:07:16|37|20|97|19|7|attack|2
VLNJX|ckhKB|3|265|2024-12-05 15:03:44|33|20|47|9|8|recover|2
VLNJX|ckhKB|3|384|2024-12-02 14:40:40|24|20|61|2|9|recover|1
</pre>

<pre>
sqlite> .schema event
CREATE TABLE event (event_id INTEGER PRIMARY KEY, ts TIMESTAMP, character_id INTEGER, player_id INTEGER, character_id_dst INTEGER, player_id_dst INTEGER, action_type VARCHAR(20), action_value INTEGER);
sqlite> .schema player
CREATE TABLE player (player_id INTEGER, first_name VARCHAR(20), last_name VARCHAR(20), points INTEGER, player_rank INTEGER);
</pre>
