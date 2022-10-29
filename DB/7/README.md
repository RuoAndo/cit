# 0. 好きな食べ物のデータベースを作成

人のテーブルを作成
<pre>
create table favarite_food (person_id SMALLINT UNSINGED, food varchar(20), constraint pk_favorite_food primary key (person_id, food), constraint fk_fav_food_person_id foreign key (person_id) references person (person_id));
</pre>

好物のテーブルを作成
<pre>
create table favarite_food (person_id SMALLINT UNSINGED, food varchar(20), constraint pk_favorite_food primary key (person_id, food), constraint fk_fav_food_person_id foreign key (person_id) references person (person_id));
</pre>

<img src="create-table.png">

Sato Hanakoのデータを格納
<pre>
insert into person (fname, lname, eye_color, birth_date) values('hanako', 'sato', 'BR', '1972-10-27');
</pre>

Taro Yamadaのデータを格納
<pre>
insert into person (fname, lname, eye_color, birth_date) values('taro', 'yamada', 'BR', '1972-05-27');
</pre>

<img src="insert.png">


