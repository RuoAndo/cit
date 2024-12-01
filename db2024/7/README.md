# テーブル項目修正 (2024-12-01)
<img src="ER_7.jpeg">

# playerテーブルとeventテーブルの結合
<pre>
sqlite> SELECT player.first_name, player.last_name, player.player_rank, event.* FROM event JOIN player ON event.player_id = player.player_id WHERE event.player_id = 20 LIMIT 5;
VLNJX|ckhKB|3|6|2024-12-04 12:09:59|7|20|20|8|28|recover
VLNJX|ckhKB|3|21|2024-12-04 10:47:04|1|20|53|1|19|recover
VLNJX|ckhKB|3|25|2024-12-05 10:33:37|87|20|33|19|3|attack
VLNJX|ckhKB|3|36|2024-12-04 11:49:38|76|20|5|19|19|attack
VLNJX|ckhKB|3|39|2024-12-02 10:08:17|97|20|44|2|21|attack
</pre>
