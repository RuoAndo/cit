<img src="players.png">
<img src="characters.png">

# 6.1 SQL tableの作成 (player, character, event)

<pre>
> python 6_1_create_character_table.py
> python 6_2_create_player_table.py
> python 6_3_create_event_table.py
</pre>
  
# 6.2 SQL スキーマの表示

<pre>
sqlite> .schema player
CREATE TABLE player (player_id INTEGER, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));
sqlite> .schema character
CREATE TABLE character (character_id INTEGER, player_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);
sqlite> .schema event
CREATE TABLE event (event_id INTEGER PRIMARY KEY, ts TIMESTAMP, character_id INTEGER, player_id INTEGER, character_id_dst INTEGER, player_id_dst INTEGER, action_type VARCHAR(20), action_value INTEGER);
</pre>

<img src="dora_begi.png" width=50%>
<img src="dora2.png" width=50%>
<img src="dora3.png" width=50%>
  
# 6.3 SQL playerテーブルとeventテーブルのJOIN

<pre>
sqlite> SELECT player.fname, player.lname, event.* FROM event JOIN player ON event.player_id = player.player_id WHERE event.player_id = 20 LIMIT 5;
xYvoT|gUPpW|12|2024-11-26 11:05:06|20|20|39|18|7|attack
xYvoT|gUPpW|22|2024-11-23 13:25:28|28|20|21|10|24|attack
xYvoT|gUPpW|41|2024-11-24 13:13:08|28|20|55|11|20|recover
xYvoT|gUPpW|60|2024-11-25 10:00:56|54|20|57|3|3|attack
xYvoT|gUPpW|101|2024-11-23 14:58:00|86|20|5|16|18|attack
</pre>

# 6.4 SQLの構文（テクニック）

<pre>
1. グループ化と集計
2. サブクエリ
3. 結合
4. 条件付きロジック
5. トランザクション
6. インデックスと制約
7. ビュー
8. メタデータ
9. 解析関数
</pre>

# 6.5 DataFrame 1対1結合

<pre>
1対1結合
import pandas as pd
import numpy as np

df1 = pd.DataFrame({'employee': ['Bob', 'Jake', 'Lisa', 'Sue'],
                    'group': ['Accounting', 'Engineering',
                              'Engineering', 'HR']})
df2 = pd.DataFrame({'employee': ['Lisa', 'Bob', 'Jake', 'Sue'],
                    'hire_date': [2004, 2008, 2012, 2014]})
</pre>

# 6.6 DataFrame 1対多結合

<pre>
1対多結合
import pandas as pd
df4 = pd.DataFrame({'group': ['Accounting', 'Engineering', 'HR'],
                    'supervisor': ['Carly', 'Guido', 'Steve']})
df5 = pd.merge(df3,df4)
</pre>

# 6.7 DataFrame 多対多結合

<pre>
import pandas as pd
df5 = pd.DataFrame({'group': ['Accounting', 'Accounting',
                              'Engineering', 'Engineering', 'HR', 'HR'],
                    'skills': ['math', 'spreadsheets', 'software', 'math',
                               'spreadsheets', 'organization']}
</pre>
