# 第２正規形(2NF)の作成

<pre>
sqlite> SELECT film_id, title, description FROM film LIMIT 5;
1|ACADEMY DINOSAUR|A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies
2|ACE GOLDFINGER|A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China
3|ADAPTATION HOLES|A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon Factory
4|AFFAIR PREJUDICE|A Fanciful Documentary of a Frisbee And a Lumberjack who must Chase a Monkey in A Shark Tank
5|AFRICAN EGG|A Fast-Paced Documentary of a Pastry Chef And a Dentist who must Pursue a Forensic Psychologist in The Gulf of Mexico
</pre>

<pre>
sqlite> SELECT actor_id, film_id, last_update FROM film_actor LIMIT 5;
1|1|2020-12-23 07:13:43
1|23|2020-12-23 07:13:43
1|25|2020-12-23 07:13:43
1|106|2020-12-23 07:13:43
1|140|2020-12-23 07:13:43
</pre>
