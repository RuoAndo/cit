# 1. selectの処理時間を計測してプロット

<img src="2023-11-12-01.png" width=120%>

# 2. actorとfilm_idを内部結合
<pre>
sqlite> SELECT actor.actor_id, first_name, last_name, film_id FROM actor JOIN film_actor ON actor.actor_id = film_actor.actor_id LIMIT 5;
1|PENELOPE|GUINESS|1
1|PENELOPE|GUINESS|23
1|PENELOPE|GUINESS|25
1|PENELOPE|GUINESS|106
1|PENELOPE|GUINESS|140
</pre>
  
# 3. actorとfilm_idを内部結合してランダムに5件表示

<pre>
sqlite> SELECT actor.actor_id, first_name, last_name, film_id FROM actor JOIN film_actor ON actor.actor_id = film_actor.actor_id ORDER BY RANDOM() LIMIT 5;
133|RICHARD|PENN|342
70|MICHELLE|MCCONAUGHEY|823
120|PENELOPE|MONROE|57
85|MINNIE|ZELLWEGER|421
188|ROCK|DUKAKIS|849
sqlite> SELECT actor.actor_id, first_name, last_name, film_id FROM actor JOIN film_actor ON actor.actor_id = film_actor.actor_id ORDER BY RANDOM() LIMIT 5;
94|KENNETH|TORN|712
155|IAN|TANDY|359
3|ED|CHASE|17
107|GINA|DEGENERES|162
181|MATTHEW|CARREY|286
</pre>

# 4. actorとfilm_idを内部結合して、actor名ごとにカウント（actorが出演している数を数える）

<pre>
sqlite> SELECT actor.actor_id, first_name, last_name, film_id, count(*) from actor JOIN film_actor ON actor.actor_id = film_actor.actor_id GROUP BY first_name HAVING count(*) > 1 LIMIT 5;
71|ADAM|GRANT|26|40
165|AL|GARLAND|72|26
173|ALAN|DREYFUSS|49|27
125|ALBERT|NOLTE|62|64
29|ALEC|WAYNE|10|29
</pre>

