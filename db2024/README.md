# tableの作成 (player, character, event)

<pre>
> python 6_1_create_character_table.py
> python 6_2_create_player_table.py
> python 6_3_create_event_table.py
</pre>
  
# スキーマの表示

<pre>
sqlite> .schema player
CREATE TABLE player (player_id INTEGER, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));
sqlite> .schema character
CREATE TABLE character (character_id INTEGER, player_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);
sqlite> .schema event
CREATE TABLE event (event_id INTEGER PRIMARY KEY, ts TIMESTAMP, character_id INTEGER, player_id INTEGER, character_id_dst INTEGER, player_id_dst INTEGER, action_type VARCHAR(20), action_value INTEGER);
</pre>
  
# playerテーブルとeventテーブルのJOIN

<pre>
sqlite> SELECT player.fname, player.lname, event.* FROM event JOIN player ON event.player_id = player.player_id WHERE event.player_id = 20 LIMIT 5;
xYvoT|gUPpW|12|2024-11-26 11:05:06|20|20|39|18|7|attack
xYvoT|gUPpW|22|2024-11-23 13:25:28|28|20|21|10|24|attack
xYvoT|gUPpW|41|2024-11-24 13:13:08|28|20|55|11|20|recover
xYvoT|gUPpW|60|2024-11-25 10:00:56|54|20|57|3|3|attack
xYvoT|gUPpW|101|2024-11-23 14:58:00|86|20|5|16|18|attack
</pre>
