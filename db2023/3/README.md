# 1. csvファイルの読み込み
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
