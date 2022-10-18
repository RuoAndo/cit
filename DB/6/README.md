# 0 sakila DBを開く

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

# 1 重複を取り除く

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
5

