# csvファイルの読み込み
<pre>
sqlite> .mode csv
sqlite> .import ./BostonHousing.csv boston
sqlite> .schema boston
CREATE TABLE IF NOT EXISTS "boston"(
"crim" TEXT, "zn" TEXT, "indus" TEXT, "chas" TEXT,
 "nox" TEXT, "rm" TEXT, "age" TEXT, "dis" TEXT,
 "rad" TEXT, "tax" TEXT, "ptratio" TEXT, "b" TEXT,
 "lstat" TEXT, "medv" TEXT);
</pre>

#  Boston Housing データセットの項目の説明
<pre>
CRIM： 町別の「犯罪率」
ZN： 25,000平方フィートを超える区画に分類される住宅地の割合＝「広い家の割合」
INDUS： 町別の「非小売業の割合」
CHAS： チャールズ川のダミー変数（区画が川に接している場合は1、そうでない場合は0）＝「川の隣か」
NOX： 「NOx濃度（0.1ppm単位）」＝一酸化窒素濃度（parts per 10 million単位）。この項目を目的変数とする場合もある
RM： 1戸当たりの「平均部屋数」
AGE： 1940年より前に建てられた持ち家の割合＝「古い家の割合」
DIS： 5つあるボストン雇用センターまでの加重距離＝「主要施設への距離」
RAD： 「主要高速道路へのアクセス性」の指数
TAX： 10,000ドル当たりの「固定資産税率」
PTRATIO： 町別の「生徒と先生の比率」
B： 「1000(Bk - 0.63)」の二乗値。Bk＝「町ごとの黒人の割合」を指す
LSTAT： 「低所得者人口の割合」
MEDV：「住宅価格」（1000ドル単位）の中央値。通常はこの数値が目的変数として使われる
</pre>

# 課題 データベースから、PTRATIO： 町別の「生徒と先生の比率」の列を取り出しなさい。
