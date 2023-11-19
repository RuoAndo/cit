<img src="sakila_schemes.jpg">

# 1. 第２正規形(2NF)の作成とCSVファイルへのエクスポート
1-1. filmテーブルの表示（5件表示）
<pre>
sqlite> SELECT film_id, title, description FROM film LIMIT 5;
1|ACADEMY DINOSAUR|A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies
2|ACE GOLDFINGER|A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China
3|ADAPTATION HOLES|A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon Factory
4|AFFAIR PREJUDICE|A Fanciful Documentary of a Frisbee And a Lumberjack who must Chase a Monkey in A Shark Tank
5|AFRICAN EGG|A Fast-Paced Documentary of a Pastry Chef And a Dentist who must Pursue a Forensic Psychologist in The Gulf of Mexico
</pre>
1-2. film_actorテーブルの表示（5件表示）
<pre>
sqlite> SELECT actor_id, film_id, last_update FROM film_actor LIMIT 5;
1|1|2020-12-23 07:13:43
1|23|2020-12-23 07:13:43
1|25|2020-12-23 07:13:43
1|106|2020-12-23 07:13:43
1|140|2020-12-23 07:13:43
</pre>
1-3. filmテーブルとfilm_actorを内部結合して5件表示
<pre>
sqlite> SELECT F.film_id, F.title, F.description, FA.actor_id, FA.last_update FROM film F JOIN film_actor FA ON F.film_id = FA.film_id LIMIT 5;
1|ACADEMY DINOSAUR|A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies|1|2020-12-23 07:13:43
23|ANACONDA CONFESSIONS|A Lacklusture Display of a Dentist And a Dentist who must Fight a Girl in Australia|1|2020-12-23 07:13:43
25|ANGELS LIFE|A Thoughtful Display of a Woman And a Astronaut who must Battle a Robot in Berlin|1|2020-12-23 07:13:43
106|BULWORTH COMMANDMENTS|A Amazing Display of a Mad Cow And a Pioneer who must Redeem a Sumo Wrestler in The Outback|1|2020-12-23 07:13:43
140|CHEAPER CLYDE|A Emotional Character Study of a Pioneer And a Girl who must Discover a Dog in Ancient Japan|1|2020-12-23 07:13:43
</pre>
1.4 filmテーブルとfilm_actorを内部結合してCSVファイルにエクスポート(6_2NF_1.csv) 2NF:第2正規形
<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023\6> .\sqlite3.exe .\sakila_master.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> .headers on
sqlite> .mode csv
sqlite> .once 6_2NF_1.csv
sqlite> SELECT F.film_id, F.title, F.description, FA.actor_id, FA.last_update FROM film F JOIN film_actor FA ON F.film_id = FA.film_id;
</pre>
1.5 作成したCSVファイルの内容を5件表示
<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023\6> head -n 5 .\6_2NF_1.csv
film_id,title,description,actor_id,last_update
1,"ACADEMY DINOSAUR","A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies",1,"2020-12-23 07:13:43"
23,"ANACONDA CONFESSIONS","A Lacklusture Display of a Dentist And a Dentist who must Fight a Girl in Australia",1,"2020-12-23 07:13:43"
25,"ANGELS LIFE","A Thoughtful Display of a Woman And a Astronaut who must Battle a Robot in Berlin",1,"2020-12-23 07:13:43"
106,"BULWORTH COMMANDMENTS","A Amazing Display of a Mad Cow And a Pioneer who must Redeem a Sumo Wrestler in The Outback",1,"2020-12-23 07:13:43"
</pre>

# 2. 第１正規形(1NF)の作成とCSVファイルへのエクスポート
2.1 CSVファイルから第２正規形のテーブルをインポートして、テーブルの名前をnf (normal form)として、内容を3件表示
<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023\6> .\sqlite3.exe .\sakila_master.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> .mode csv
sqlite> .import 6_2NF_1.csv nf
sqlite> .schema nf
CREATE TABLE IF NOT EXISTS "nf"(
"film_id" TEXT, "title" TEXT, "description" TEXT, "actor_id" TEXT,
 "last_update" TEXT);
sqlite> select * from nf LIMIT 3;
1,"ACADEMY DINOSAUR","A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies",1,"2020-12-23 07:13:43"
23,"ANACONDA CONFESSIONS","A Lacklusture Display of a Dentist And a Dentist who must Fight a Girl in Australia",1,"2020-12-23 07:13:43"
25,"ANGELS LIFE","A Thoughtful Display of a Woman And a Astronaut who must Battle a Robot in Berlin",1,"2020-12-23 07:13:43"
</pre>
2.2 インポートしたnfテーブルとactorテーブルと内部結合して第１正規形(1NF)を作成し、5件表示
<pre>
sqlite> SELECT A.actor_id, A.first_name, A.last_name, A.last_update, nf.film_id, nf.last_update, nf.title, nf.description FROM actor A JOIN nf ON A.actor_id = nf.actor_id LIMIT 5;
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",1,"2020-12-23 07:13:43","ACADEMY DINOSAUR","A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",23,"2020-12-23 07:13:43","ANACONDA CONFESSIONS","A Lacklusture Display of a Dentist And a Dentist who must Fight a Girl in Australia"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",25,"2020-12-23 07:13:43","ANGELS LIFE","A Thoughtful Display of a Woman And a Astronaut who must Battle a Robot in Berlin"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",106,"2020-12-23 07:13:43","BULWORTH COMMANDMENTS","A Amazing Display of a Mad Cow And a Pioneer who must Redeem a Sumo Wrestler in The Outback"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",140,"2020-12-23 07:13:43","CHEAPER CLYDE","A Emotional Character Study of a Pioneer And a Girl who must Discover a Dog in Ancient Japan"
</pre>
2.3 作成した第１正規形(1NF)を、CSVファイルにエクスポート(6_1NF_1.csv)
<pre>
sqlite> .headers on
sqlite> .mode csv
sqlite> .once 6_1NF_1.csv
sqlite> SELECT A.actor_id, A.first_name, A.last_name, A.last_update, nf.film_id, nf.last_update, nf.title, nf.description FROM actor A JOIN nf ON A.actor_id = nf.actor_id;
</pre>
2.3 作成したCSVファイルの内容を5件表示
<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023\6> head -n 5 .\6_1NF_1.csv
actor_id,first_name,last_name,last_update,film_id,last_update,title,description
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",1,"2020-12-23 07:13:43","ACADEMY DINOSAUR","A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",23,"2020-12-23 07:13:43","ANACONDA CONFESSIONS","A Lacklusture Display of a Dentist And a Dentist who must Fight a Girl in Australia"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",25,"2020-12-23 07:13:43","ANGELS LIFE","A Thoughtful Display of a Woman And a Astronaut who must Battle a Robot in Berlin"
1,PENELOPE,GUINESS,"2020-12-23 07:12:29",106,"2020-12-23 07:13:43","BULWORTH COMMANDMENTS","A Amazing Display of a Mad Cow And a Pioneer who must Redeem a Sumo Wrestler in The Outback"
</pre>
