# 1.playerとcharacterのテーブルを作成

<pre>
(base) C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023>python 07_insert_player_repeat.py
insert into player (player_id, fname, lname, points, rank) values('0','yvKis','JMxwm','7','X');
insert into player (player_id, fname, lname, points, rank) values('1','okcGw','Vawbp','6','I');
</pre>

<pre>
(base) C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023>python 07_insert_character_repeat.py  
</pre>

1.1 人気のcharacterを調べる

<pre>
(base) C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023>sqlite3.exe cit-db-2023-07.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> SELECT P.player_id, P.fname, P.lname, C.character_id, C.character_name, count(*) FROM player P INNER JOIN character C ON P.player_id = C.player_id GROUP BY character_name HAVING count(*) > 10;
1|ixrfv|RPAJK|316|akinator|234
1|ixrfv|RPAJK|178|begita|184
1|ixrfv|RPAJK|79|bikkuriko|207
1|ixrfv|RPAJK|240|doraemon|193
1|ixrfv|RPAJK|172|golgo|182
</pre>

<pre>
(base) C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023>sqlite3.exe cit-db-2023-07.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> SELECT P.player_id, P.fname, P.lname, C.character_id, C.character_name, count(*) FROM player P INNER JOIN character C ON P.player_id = C.player_id GROUP BY character_id HAVING count(*) > 10;
sqlite> SELECT P.player_id, P.fname, P.lname, C.character_id, C.character_name, count(*) FROM player P INNER JOIN character C ON P.player_id = C.player_id GROUP BY character_name HAVING count(*) > 10;
1|okcGw|Vawbp|8|akinator|199
1|okcGw|Vawbp|17|begita|188
1|okcGw|Vawbp|71|bikkuriko|190
1|okcGw|Vawbp|119|doraemon|222
1|okcGw|Vawbp|65|golgo|201
</pre>

