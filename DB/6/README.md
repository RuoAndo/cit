# 0. sakila DBを開く

<pre>
sqlite> .open sakila_master.db
sqlite> .tables
actor                   film                    payment
address                 film_actor              rental
category                film_category           sales_by_film_category
city                    film_list               sales_by_store
country                 film_text               staff
customer                inventory               staff_list
customer_list           language                store
</pre>

# 1. 重複を取り除く

<pre>
sqlite> .schema film_actor
CREATE TABLE film_actor (
  actor_id INT NOT NULL,
  film_id  INT NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (actor_id,film_id),
  CONSTRAINT fk_film_actor_actor FOREIGN KEY (actor_id) REFERENCES actor (actor_id) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT fk_film_actor_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE NO ACTION ON UPDATE CASCADE
);

sqlite> select actor_id from film_actor order by actor_id limit 5;
1
1
1
1
1
</pre>

actor_idの重複を削除する

<pre>
sqlite> select distinct actor_id from film_actor order by actor_id limit 5;
1
2
3
4
</pre>

# 2. テーブルのリンク

<pre>
sqlite> select c.first_name, c.last_name, time(rental.rental_date) rental_time from customer c inner join rental on c.customer_id = rental.customer_id where date(rental.rental_date) = '2005-06-14';
JEFFERY|PINSON|22:53:33
ELMER|NOE|22:55:13
MINNIE|ROMERO|23:00:34
MIRIAM|MCKINNEY|23:07:08
DANIEL|CABRAL|23:09:38
TERRANCE|ROUSH|23:12:46
JOYCE|EDWARDS|23:16:26
GWENDOLYN|MAY|23:16:27
CATHERINE|CAMPBELL|23:17:03
MATTHEW|MAHAN|23:25:58
HERMAN|DEVORE|23:35:09
AMBER|DIXON|23:42:56
TERRENCE|GUNDERSON|23:47:35
SONIA|GREGORY|23:50:11
CHARLES|KOWALSKI|23:54:34
JEANETTE|GREENE|23:54:46
</pre>
