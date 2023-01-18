<img src="json1.JPG" width=70%>

# 0. CSVからJSONファイルへ書き換え
太郎さんは２つキャラを、花子さんは１つのキャラを持っている
CSV (comma separated value) 
person_ID, first_name, last_name, character_ID, character_name, HP, MP, EXP

CSV
<pre>
(1, 'taro', 'yamada', 1, 'doraemon', 14, 10, 0)
(1, 'taro', 'yamada', 2, 'akinator', 20, 5, 0)
(2, 'hanako', 'sato', 2, 'akinator', 16, 5, 0)
</pre>

JSON
<pre>
{
 "person_id" : "1",
 "first_name" : "yamada",
 "last_name": "taro", 
	"characters" : [
		{
			charater_id : "1",
			character_name : "doraemon", 
			HP : "15",
			MP : "10",
			EXP : "0"
		},
		{
			charater_id : "2",
			character_name : "akinator", 
			HP : "10",
			MP : "15",
			EXP : "5"
		}
	]
}

{
"person_id" : "2", 
 "first_name" : "hanako",
 "last_name": "sato",
	"characters" : [
		{
			charater_id : "1",
			character_name : "doraemon", 
			HP : "15",
			MP : "10",
			EXP : "0"
		}
	]
}	 
</pre>

# 1. プログラム構成と発行しているSQL文

<img src="kousei.png">

1. loop_join.py
一定時間ごとに、各キャラクタのステータスを表示し、HPをランダムに回復させる

<img src="bc.png">

<pre>
	1-1. select * from player inner join character on character.person_id = player.person_id;
	1-2. update character set HP=3061 where character_id = 1 and person_id=1;
	1-3. update character set HP=3109 where character_id = 2 and person_id=1;
	1-4. update character set HP=3089 where character_id = 2 and person_id=2;
</pre>

2. warikomi2.ps1
各キャラクタのHPを減少させる

<img src="nobita2.png" width=7%>

<pre>
	2-1. update character set HP=3060 where character_id = 2 and person_id=2;
	2-2. insert into events (person_id, character_id, character_name, event_type, event_time, event_counter, HP) values(2,2,'akinator','attack','2023-01-18 	16:20:28.796926',213,3074);
</pre>

3. loop_show_events
今まで発生したイベントを表示する

<img src="gantz.jpg" width=5%>

<pre>
	3-1. select * from events
</pre>

4. show_event.py
今までの、キャラクタのHPの推移をグラフで表示する

<pre>
	4-1. select * from events where person_ID = 1 and character_ID = 1
</pre>



