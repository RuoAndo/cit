
# playerテーブルとschemaテーブルを作成

<pre>
5_1_create_character_table.ipynb
5_2_create_player_table.ipynb
</pre>
  
<pre>
sqlite> .schema player
CREATE TABLE player (player_id INTEGER, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));
sqlite> .schema character
CREATE TABLE character (character_id INTEGER, player_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);
</pre>

# データ表示

<pre>
sqlite> select * from player limit 5;
0|Mjzxr|CZsIh|86|P
1|sMBWd|Dsvhv|53|B
2|IczjS|vmFSp|45|Y
3|sJFRD|CBCQf|35|P
4|ORsLl|NnvBJ|35|P
sqlite> select * from character limit 5;
0|15|doraemon|14|54|14
1|3|doraemon|21|47|42 
2|19|doraemon|38|16|20
3|5|golgo|60|69|65    
4|18|begita|26|56|23  
</pre>

# playerテーブルとschemaテーブルの結合

<pre>
sqlite> SELECT player.player_id, player.fname, player.lname, player.points, player.rank, character.character_id, character.character_name,  character.HP, character.MP, character.EXP FROM player JOIN character ON player.player_id = character.player_id LIMIT 10;
1|sMBWd|Dsvhv|53|B|5|doraemon|16|54|83
1|sMBWd|Dsvhv|53|B|17|bikkuriko|20|13|47
1|sMBWd|Dsvhv|53|B|21|doraemon|31|60|63
1|sMBWd|Dsvhv|53|B|86|doraemon|13|90|32
2|IczjS|vmFSp|45|Y|44|akinator|39|23|56
2|IczjS|vmFSp|45|Y|65|doraemon|33|89|31
2|IczjS|vmFSp|45|Y|71|bikkuriko|75|88|36
2|IczjS|vmFSp|45|Y|84|akinator|46|86|2
2|IczjS|vmFSp|45|Y|88|begita|95|90|77
2|IczjS|vmFSp|45|Y|90|golgo|18|98|15
</pre>
