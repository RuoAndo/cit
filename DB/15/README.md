# SQLデータベースにある（大量の）キャラクタを可視化する

<img src="h.png">

2.batを実行した後、下記の順番で実行

<img src="gamen.jpg">

<pre>
loop_join.py: 一定期間ごとにHPとEXPを加算
attack.py: 
plot_character.py: 全キャラクターのステータスを表示
</pre>

# 異常検知：ヤバいキャラクタを検出

<img src="b.png">

<pre>
plot_character_2.py: K平均法（クラスタは１つ）
を実行する
</pre>
<img src="km.png">
