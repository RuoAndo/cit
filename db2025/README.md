# 授業で扱ったSQL文　まとめ

# A. 非相関サブクエリ（単一値との比較・集計）
1

対象SQL
SELECT title, rental_rate FROM film WHERE rental_rate > (SELECT AVG(rental_rate) FROM film);
説明
内側で film 全体の rental_rate 平均を1回だけ計算し、その平均より高い行だけ外側で抽出。結果は「平均より割高な映画」の一覧（タイトルと料金）。

2

対象SQL
SELECT customer_id, rental_date FROM rental WHERE rental_date = (SELECT MAX(rental_date) FROM rental);
説明
内側で rental 全体の最新日時（MAX）を1回計算し、その日時と一致するレンタル行を返す。最新日時に複数レンタルがあれば全件出る（=「最後に借りた顧客」ではなく「最後の時刻のレコード」）。

3

対象SQL
SELECT title, length FROM film WHERE length > (SELECT AVG(length) FROM film);
説明
film 全体の平均上映時間を1回計算し、平均より長い作品だけ抽出。結果は長編寄りの映画一覧。

4

対象SQL
SELECT title, rental_rate FROM film WHERE rental_rate = (SELECT MAX(rental_rate) FROM film);
説明
film の最大レンタル料金を1回求め、その最大値と同じ rental_rate の映画を抽出。最大料金が同率なら複数作品が返る。

5

対象SQL
SELECT customer_id FROM payment GROUP BY customer_id HAVING SUM(amount) > (SELECT AVG(amount) FROM payment);
説明
外側で顧客別に支払い合計（SUM）を作り、内側で payment 全体の平均支払額（1レコード平均）を出して比較。
「顧客別合計」vs「1回あたり平均」なので、意図が「平均より多く支払う顧客」なら 13番の形が自然。

6

対象SQL
SELECT f1.title FROM film f1 WHERE EXISTS (SELECT 1 FROM film f2 WHERE f2.length < f1.length);
説明
各映画 f1 について、より短い映画 f2 が1本でも存在すれば真。最短上映時間の映画だけが除外され、それ以外はほぼ全部出る傾向（「最短以外を全部出す」に近い）。

7

対象SQL
SELECT MAX(amount), MIN(amount), AVG(amount), SUM(amount), COUNT(*) FROM payment;
説明
payment 全体の統計値を1行で出す集計。売上総額（SUM）・取引回数（COUNT）・単価の平均（AVG）・最大/最小が同時にわかる。

# B. 相関サブクエリ（行ごとに再計算）
8

対象SQL
SELECT f.title, f.rental_rate FROM film f WHERE f.rental_rate > (SELECT AVG(f2.rental_rate) FROM film f2 WHERE f2.length = f.length);
説明
外側の各映画 f の length を使って、内側で「同じlength作品群の平均 rental_rate」を計算（行ごとに平均が変わる）。
結果は「同尺の中で平均より割高な作品」。

9

対象SQL
SELECT p1.payment_id, p1.customer_id, p1.amount FROM payment p1 WHERE p1.amount > (SELECT AVG(p2.amount) FROM payment p2 WHERE p2.customer_id = p1.customer_id);
説明
各支払い p1 に対し、その顧客の支払い平均（顧客内AVG）を再計算して比較。
結果は「その顧客にとって高めの支払い（いつもより高額な取引）」の抽出。

10

対象SQL
SELECT r1.customer_id, r1.rental_date FROM rental r1 WHERE r1.rental_date = (SELECT MAX(r2.rental_date) FROM rental r2 WHERE r2.customer_id = r1.customer_id);
説明
顧客ごとに最新レンタル日時（MAX）を求め、その日時と一致するレンタル行を返す。
顧客が同時刻に複数借りていれば複数行になる（顧客別「最終レンタル時刻の明細」）。

11

対象SQL
SELECT c.first_name, c.last_name CASE WHEN active = 0 THEN 0 ELSE (SELECT count(*) FROM rental r WHERE r.customer_id = c.customer_id) END NUM_rentals FROM customer c;
説明
意図は「非アクティブなら0、アクティブなら顧客別レンタル回数」を返すこと。
ただし文法上 c.last_name の後にカンマが必要。正しくは SELECT c.first_name, c.last_name, CASE WHEN ... END AS num_rentals ...。

# C. IN / 多段IN（集合フィルタ）
12

対象SQL
SELECT title FROM film WHERE film_id IN (SELECT film_id FROM film_actor WHERE actor_id IN (SELECT actor_id FROM actor WHERE last_name = 'SMITH'));
説明
(1) actor から last_name='SMITH' の actor_id を集める
(2) film_actor からその actor_id が出演する film_id を集める
(3) film からその film_id の title を出す
=「SMITH姓の俳優が出ている映画一覧」。

# D. 派生表（FROMサブクエリ）・二段集計
13

対象SQL
SELECT customer_id, SUM(amount) AS total_amount FROM payment GROUP BY customer_id HAVING SUM(amount) > (SELECT AVG(total_amount) FROM (SELECT SUM(amount) AS total_amount FROM payment GROUP BY customer_id) AS t);
説明
内側の派生表で「顧客別合計（total_amount）」を全顧客分作り、その平均をさらに計算。外側で顧客別合計が平均より大きい顧客だけ残す。
「平均より多く支払う顧客」を“顧客単位”で正しく比較している。

14

対象SQL
SELECT cust.last_name, ",", cust.first_name FROM (select first_name, last_name, email FROM customer WHERE first_name = 'JESSIE') cust;
説明
派生表 cust は first_name='JESSIE' に絞った顧客集合。外側は表示整形（姓・カンマ・名を別列で出す）。検索結果を“中間表化して再利用する”練習。

15

対象SQL
SELECT city_id, city FROM city WHERE country_id <> (SELECT country_id FROM country WHERE country = 'India') LIMIT 5;
説明
country から India の country_id を1つ取得し、city からそのID以外の都市を抽出。
「特定国を除外する」パターン（LIMIT 5は表示用）。

# E. ランキング・件数条件
16

対象SQL
SELECT title FROM film WHERE film_id = (SELECT film_id FROM inventory JOIN rental USING (inventory_id) GROUP BY film_id ORDER BY COUNT(*) DESC LIMIT 1);
説明
inventory と rental を結合し、film_id ごとにレンタル回数を COUNT(*) で数える。回数が最大の film_id を1件だけ取り、その film の title を返す。
同率1位が複数でも LIMIT 1 なので“どれか1本”になる。

17

対象SQL
SELECT customer_id, count(*) FROM rental GROUP BY customer_id ORDER BY 2 DESC LIMIT 5;
説明
rental を customer_id でグループ化して件数を出し、件数降順で上位5顧客を抽出。
「最も借りている顧客」ランキング。

18

対象SQL
SELECT c.first_name, c.last_name FROM customer c WHERE 20 = (SELECT count(*) FROM rental r WHERE r.customer_id = c.customer_id) LIMIT 10;
説明
各顧客 c について、その顧客のレンタル件数を数え、20件ちょうどの顧客だけ抽出。
相関サブクエリで “件数が条件に一致する顧客” を探す例。

# F. JOIN（一覧化・多表結合）
19

対象SQL
SELECT f.film_id, f.title, i.inventory_id FROM film f LEFT OUTER JOIN inventory i ON f.film_id = i.film_id;
説明
film を基準に全映画を出し、在庫があれば inventory_id を付ける。
在庫がない映画も残るので「在庫ゼロ映画」も見つけられる（inventory_id が NULL）。

20

対象SQL
SELECT s.staff_id, s.first_name, a.address FROM staff s LEFT OUTER JOIN address a ON s.address_id = a.address_id;
説明
staff を全件出し、対応する住所があれば address を付与。
参照先が欠けているスタッフがいれば address が NULL になる。

21

対象SQL
SELECT ca.category_id, ca.name, fc.film_id FROM category ca LEFT OUTER JOIN film_category fc ON ca.category_id = fc.category_id;
説明
category を全件出し、カテゴリに属する映画があれば film_id を並べる。
映画が1本もないカテゴリは film_id が NULL になり判定しやすい。

22

対象SQL
SELECT a.address_id, c.city FROM address a RIGHT OUTER JOIN city c ON a.city_id = c.city_id;
説明
city を全件残し、そこに属する address があれば address_id を付ける。
住所が存在しない都市も出る（address_id が NULL）。SQLiteなどRIGHT JOIN非対応では city LEFT JOIN address に書き換える。

23

対象SQL
SELECT fc.film_id, c.name FROM film_category fc RIGHT OUTER JOIN category c ON fc.category_id = c.category_id;
説明
category を全件残し、映画があるカテゴリは film_id が出る。
映画ゼロカテゴリ検出用。RIGHT JOIN非対応DBは LEFT に書き換え。

24

対象SQL
SELECT i.inventory_id, f.title FROM inventory i RIGHT OUTER JOIN film f ON i.film_id = f.film_id;
説明
film を全件残し、在庫があれば inventory_id を付与。
在庫ゼロ映画の検出に使える（inventory_id が NULL）。RIGHT JOIN非対応DBは LEFT に書き換え。

25

対象SQL
SELECT r.rental_id, c.first_name FROM rental r RIGHT OUTER JOIN customer c ON r.customer_id = c.customer_id;
説明
customer を全件残し、レンタルがあれば rental_id を付ける。
レンタル未経験顧客は rental_id が NULL。RIGHT JOIN非対応DBは LEFT に書き換え。

26

対象SQL
SELECT c.first_name, c.last_name, ct.city, sum(p.amount), count(*) FROM payment p INNER JOIN customer c ON p.customer_id = c.customer_id INNER JOIN address a ON c.address_id = a.address_id INNER JOIN city ct ON a.city_id = ct.city_id GROUP BY c.first_name, c.last_name, ct.city LIMIT 10;
説明
支払い p を起点に顧客→住所→都市まで結合し、氏名＋都市単位で支払い合計と件数を集計。
同姓同名がいる可能性を考えると、本来は customer_id でGROUP BYするのが安全（練習としては結合と集計の例）。

27

対象SQL
SELECT c.first_name, c.last_name, a.address FROM customer c INNER JOIN address a ON c.address_id = a.address_id WHERE a.postal_code = 52137;
説明
customer と address を結合し、郵便番号が指定値の顧客だけ抽出。
住所属性（postal_code）で顧客をフィルタする典型例。

28

対象SQL
SELECT actor.actor_id, first_name, last_name, film_id FROM actor INNER JOIN film_actor on actor.actor_id = film_actor.actor_id LIMIT 10;
説明
actor と film_actor を結合し、俳優がどの film_id に出演しているかを一覧化。
多対多（俳優×映画）の中間表を辿る基本。

# G. 外部結合（未一致も含める意図が主）
29

対象SQL
SELECT c.customer_id, c.first_name, r.rental_id FROM customer c LEFT OUTER JOIN rental r ON c.customer_id = r.customer_id;
説明
顧客を全件出し、レンタルがあれば rental_id を付与。
レンタルがない顧客も残るため「未レンタル顧客」の抽出や監査に使う（WHERE r.rental_id IS NULL で未レンタルだけにできる）。

# H. CASE（分類・フラグ・条件付き集計）
30

対象SQL
SELECT payment_id, amount, CASE WHEN amount >= 8 THEN 'high' WHEN amount >= 4 THEN 'mid' ELSE 'low' END AS amount_band FROM payment;
説明
amount を閾値で3区分し、カテゴリラベルを作る。
この結果を派生表にして GROUP BY amount_band すると帯別件数や売上が簡単に出せる。

31

対象SQL
SELECT rental_id, rental_date, return_date, CASE WHEN return_date IS NULL THEN 1 ELSE 0 END AS is_open FROM rental;
説明
返却日NULLを「貸出中」とみなしてフラグ列を作成。
後段で WHERE is_open=1 相当の条件に使ったり、未返却件数の集計に使える。

32

対象SQL
SELECT s.store_id, SUM(CASE WHEN r.return_date IS NULL THEN 1 ELSE 0 END) AS open_rentals FROM rental r JOIN staff s ON s.staff_id = r.staff_id GROUP BY s.store_id;
説明
rental を staff 経由で店舗に紐づけ、未返却だけを 1 として足し上げることで店舗別未返却数を算出。
COUNT(*)だと全レンタル数になるので、条件付き集計としてSUM(CASE…)を使っている。

33

対象SQL
SELECT customer_id, COUNT(*) AS payments_total, SUM(CASE WHEN amount >= 5 THEN 1 ELSE 0 END) AS payments_ge_5 FROM payment GROUP BY customer_id;
説明
顧客別に総支払い回数と、一定額以上の支払い回数を同時に出す。
payments_ge_5 * 1.0 / payments_total のように比率を作れば“高額支払い傾向”の指標になる。

34

対象SQL
SELECT c.customer_id, c.first_name, c.last_name, CASE WHEN EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = c.customer_id AND r.return_date IS NULL) THEN 'has_open' ELSE 'no_open' END AS open_status FROM customer c;
説明
顧客ごとに未返却レンタルの存在を確認し、状態ラベルを付与。
EXISTSは「1件でもあれば真」なので件数を数えるより軽く済むことが多い。

35

対象SQL
SELECT rental_id, rental_date, return_date FROM rental ORDER BY CASE WHEN return_date IS NULL THEN 0 ELSE 1 END, rental_date DESC;
説明
まず未返却（0）を先頭に、その次に返却済み（1）を並べる優先順位ソート。
同じ優先度の中では貸出日が新しい順に並ぶため、対応が必要な案件を上に集める用途。

36

対象SQL
SELECT r.rental_id, r.customer_id, CASE WHEN DATEDIFF(COALESCE(r.return_date, CURRENT_DATE), r.rental_date) >= 7 THEN 'late' ELSE 'ok' END AS late_flag FROM rental r;
説明
返却済みなら返却日、未返却なら今日を使って経過日数を計算し、7日以上を延滞扱いにする。
延滞抽出したい場合は WHERE DATEDIFF(COALESCE(...), ...) >= 7 と同じ条件をWHEREに置く。

37

対象SQL
SELECT first_name, last_name, CASE WHEN active = 1 THEN 'ACTIVE' ELSE 'INACTIVE' END active_type FROM customer LIMIT 10;
説明
activeフラグを文字ラベルへ変換し、人間が読みやすい形で一覧化。
実務では active=0 のみをWHEREで絞って休眠顧客一覧に使う。

# I. NULL対策・日時処理
38

対象SQL
SELECT rental_id, rental_date, return_date, DATEDIFF(COALESCE(return_date, CURRENT_DATE), rental_date) AS days_out FROM rental;
説明
未返却でも日数計算ができるよう、return_dateがNULLならCURRENT_DATEを採用して差分日数を出す。
延滞判定や督促対象の抽出の基礎になる。

39

対象SQL
SELECT customer_id, SUM(amount) AS total_amount, COUNT(*) AS n, SUM(amount) / NULLIF(COUNT(*), 0) AS avg_amount FROM payment GROUP BY customer_id;
説明
顧客別の売上合計・取引回数・平均単価を同時に算出。
外部結合で件数0が混じる設計でもゼロ割りにならないようNULLIFで防御している。

40

対象SQL
SELECT c.first_name, c.last_name FROM customer c WHERE EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = c.customer_id AND date(r.rental_date) < '2005-05-25');
説明
ある基準日より前のレンタル履歴が1件でもある顧客を抽出。
「初期利用者」「古参顧客」のような条件抽出の基本形（date()で日付部分に丸めて比較）。

# J. 文字条件・OR・LIKE
41

対象SQL
SELECT film_id, title, CASE WHEN title REGEXP '^[A-M]' THEN 'A-M' ELSE 'N-Z' END AS title_group FROM film;
説明
タイトル先頭文字がA〜Mにマッチするかを正規表現で判定し、グループ名を付与。
REGEXPが使えないDBでは SUBSTR(title,1,1) BETWEEN 'A' AND 'M' のように代替する。

42

対象SQL
SELECT title, rating FROM film WHERE rating = 'G' OR rating = 'PG' LIMIT 5;
説明
ratingがGまたはPGの作品を抽出し、タイトルとレーティングを返す。
OR条件の基本で、同等に rating IN ('G','PG') と書ける。

43

対象SQL
select last_name, first_name FROM customer WHERE last_name LIKE '_A_T%S';
説明
LIKEのワイルドカードで姓パターン検索。_は任意の1文字、%は任意長。
この例は「2文字目がA、4文字目がT、どこかに任意文字列が入り、最後がS」の姓を抽出。

