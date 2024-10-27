<img src="sakila-schemes.jpg">

<pre>
PS D:\cit\db2024\3> .\sqlite3.exe .\sakila_master.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.

sqlite> .tables
actor                   film                    payment
address                 film_actor              rental
category                film_category           sales_by_film_category
city                    film_list               sales_by_store
country                 film_text               staff
customer                inventory               staff_list
customer_list           language                store
</pre>

<pre>
PS D:\cit\db2024\4> .\sqlite3.exe .\sakila_master.db

SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite>
sqlite> .tables
actor                   film                    payment
address                 film_actor              rental
category                film_category           sales_by_film_category
city                    film_list               sales_by_store
country                 film_text               staff
customer                inventory               staff_list
customer_list           language                store

# テーブルの情報を取得
  
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
CREATE INDEX idx_customer_fk_store_id ON customer(store_id)
;
CREATE INDEX idx_customer_fk_address_id ON customer(address_id)
;
CREATE INDEX idx_customer_last_name ON customer(last_name)
;
CREATE TRIGGER customer_trigger_ai AFTER INSERT ON customer
 BEGIN
  UPDATE customer SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
CREATE TRIGGER customer_trigger_au AFTER UPDATE ON customer
 BEGIN
  UPDATE customer SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
 
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
CREATE INDEX idx_fk_city_id ON address(city_id)
;
CREATE TRIGGER address_trigger_ai AFTER INSERT ON address
 BEGIN
  UPDATE address SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
CREATE TRIGGER address_trigger_au AFTER UPDATE ON address
 BEGIN
  UPDATE address SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;
</pre>

# addressとcustomerのテーブルを結合
<pre>
sqlite> SELECT c.first_name, c.last_name, a.address FROM customer c JOIN address a ON c.address_id = a.address_id LIMIT 10;
MARY|SMITH|1913 Hanoi Way
PATRICIA|JOHNSON|1121 Loja Avenue
LINDA|WILLIAMS|692 Joliet Street
BARBARA|JONES|1566 Inegl Manor
ELIZABETH|BROWN|53 Idfu Parkway
JENNIFER|DAVIS|1795 Santiago de Compostela Way
MARIA|MILLER|900 Santiago de Compostela Parkway
SUSAN|WILSON|478 Joliet Way
MARGARET|MOORE|613 Korolev Drive
DOROTHY|TAYLOR|1531 Sal Drive
</pre>
