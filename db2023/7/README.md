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
sqlite> SELECT C.character_name, count(*) FROM player p INNER JOIN character C on P.player_id = C.player_id GROUP BY character_name ORDER BY count(*) DESC;
doraemon|217
akinator|215
golgo|197
bikkuriko|186
begita|185
</pre>

<pre>
(base) PS C:\Users\flare\OneDrive-2023-11-15\OneDrive\cit\db2023> .\sqlite3.exe .\cit-db-2023-07.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> SELECT C.character_name, count(*) FROM player p INNER JOIN character C on P.player_id = C.player_id GROUP BY character_name ORDER BY count(*) DESC;
bikkuriko|214
doraemon|210
akinator|210
golgo|186
begita|180
</pre>

1.2 乱数に偏りをもたせる

<pre>
import random
import matplotlib.pyplot as plt 

cycle = 1000

val_list = [1,2,3,4,5]
result_list = [random.choices(val_list)[0] for _ in range(cycle)]

print(result_list)

plt.hist(result_list)
plt.show()
</pre>

<img src="random.png">

<pre>
import random
import matplotlib.pyplot as plt 


cycle = 1000

val_list = [1,2,3,4,5]
weight_list = [10,1,1,1,1]

result_list = [random.choices(val_list, weights=weight_list)[0] for _ in range(cycle)]
print(result_list)

plt.hist(result_list)
plt.show()
</pre>
  
<img src="weighted_random.png">


<pre>
sqlite> SELECT C.character_name, count(*) FROM player p INNER JOIN character C on P.player_id = C.player_id GROUP BY character_name ORDER BY count(*) DESC;
doraemon|707
bikkuriko|89
begita|81
akinator|64
golgo|59
</pre>
