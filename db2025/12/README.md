#1. SUM(…) OVER

GROUP BY による集約とは異なり、行を保持したまま合計値を付与する解析関数。ORDER BY 指定による累積和の算出。時系列売上推移や累計値把握への利用。PARTITION BY 併用による顧客別・店舗別累積。

対応SQL：
SELECT payment_date, amount, SUM(amount) OVER (ORDER BY payment_date) AS cumulative_sales FROM payment LIMIT 10;

C/C++類似技：前計算の累積和配列（prefix sum）、std::partial_sum、走査しながら累積変数を更新する1パス集計。

#2. AVG(…) OVER

平均値を各行に付与する解析関数。PARTITION BY 指定による単位別平均。平均との差分算出による外れ値検出。

対応SQL：
SELECT customer_id, payment_id, amount, amount - AVG(amount) OVER (PARTITION BY customer_id) AS diff_from_customer_avg FROM payment LIMIT 10;

C/C++類似技：グループ別に合計と件数を保持するハッシュ、2パス集計、オンライン平均（Welford法）。

#3. RANK() OVER

同順位を許容し、順位が飛ぶ競技順位型ランキング。同額値の存在を反映した順位付け。売上順位・人気順位への適用。

対応SQL：
SELECT customer_id, payment_id, amount, RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS payment_rank FROM payment LIMIT 10;

C/C++類似技：ソート後走査による順位付け、stable_sort、座標圧縮。

#4. DENSE_RANK() OVER

同順位でも順位が飛ばない密な順位付け。連番順位の維持。順位数重視の用途。

対応SQL：
SELECT store_id, payment_id, amount, DENSE_RANK() OVER (PARTITION BY store_id ORDER BY amount DESC) AS store_rank FROM payment JOIN staff USING (staff_id) LIMIT 10;

C/C++類似技：ユニーク値ごとのrank++、std::unique、dense rank マップ。

#5. LAG(列) OVER

過去行参照の解析関数。直前行の値取得。差分計算、前回比、行動間隔分析。

対応SQL：
SELECT payment_date, amount, amount - LAG(amount) OVER (ORDER BY payment_date) AS diff_from_prev FROM payment LIMIT 10;

C/C++類似技：prev変数保持、リングバッファ、配列 i-1 参照。

#6. LEAD(列) OVER

未来行参照の解析関数。次行または指定行数先の値取得。前後比較、次回イベント判定。

対応SQL：
SELECT payment_id, payment_date, amount, LEAD(amount) OVER (ORDER BY payment_date) AS next_amount FROM payment LIMIT 10;

C/C++類似技：配列 i+1 参照、事前読込による先読み、バッファリング。

#7. NTILE(n) OVER

全体の n 等分による区分付与。分位生成。層分析。

対応SQL：
SELECT payment_id, amount, NTILE(10) OVER (ORDER BY amount DESC) AS decile FROM payment LIMIT 10;

C/C++類似技：tile=(i*n)/N+1、nth_element、ヒストグラム分割。

#8. OVER (PARTITION BY …)

解析関数の計算単位指定。グループ単位の独立計算。行保持の区切り処理。

対応SQL：
SELECT customer_id, amount, AVG(amount) OVER (PARTITION BY customer_id) AS customer_avg FROM payment LIMIT 10;

C/C++類似技：キー別グルーピング、キーソートによる区間化。

#9. OVER (ORDER BY …)

解析関数への順序付与。累積計算、順位付け、前後参照の前提。時系列文脈の導入。

対応SQL：
SELECT payment_date, SUM(amount) OVER (ORDER BY payment_date) AS cumulative_sales FROM payment LIMIT 10;

C/C++類似技：std::sort／stable_sort、整列後1パス走査。

#10. ROWS BETWEEN … AND …

ウィンドウ幅指定構文。対象範囲の明示。移動平均・移動合計。

対応SQL：
SELECT store_id, payment_date, amount, AVG(amount) OVER (PARTITION BY store_id ORDER BY payment_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3 FROM payment JOIN staff USING (staff_id) LIMIT 10;

C/C++類似技：スライディングウィンドウ、deque、尺取り法。