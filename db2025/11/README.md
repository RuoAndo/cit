# 2NF版 vs 3NF版 SQL比較

## ① 職業ごとのキャラ人数を集計したい

### 🔹 2NF版

```sql
SELECT job_name,
       COUNT(*) AS character_count
FROM character
GROUP BY job_name
ORDER BY character_count DESC;
```

### 🔹 3NF版

```sql
SELECT j.job_name,
       COUNT(*) AS character_count
FROM character c
JOIN job_master j ON c.job_id = j.job_id
GROUP BY j.job_id, j.job_name
ORDER BY character_count DESC;
```

### 💬 コメント

- SQLの見た目は似ている（JOINが増えるだけ）
- 2NF版は job_name の表記揺れが別グループとしてカウントされる
  - 例：`戦士`, `戦士 `, `戦士(剣)`
- 3NF版は job_id グループ化のため結果が安定する

---

## ② 「僧侶」を「プリースト」に一括改名したい

### 🔹 2NF版

```sql
UPDATE character
SET job_name = 'プリースト'
WHERE job_name = '僧侶';
```

### 🔹 3NF版

```sql
UPDATE job_master
SET job_name = 'プリースト'
WHERE job_name = '僧侶';
```

### 💬 コメント

- 2NF版は character に散らばる job_name を全部更新
- 表記ゆれや誤字があると更新漏れ
- 別テーブルにも job_name があれば追加更新が必要
- 3NF版は job_master の1行更新で完了
→ JOIN利用すべてが同時更新され整合性確保

---

## ③ 職業ごとの平均HP・MPを出したい

### 🔹 2NF版

```sql
SELECT job_name,
       AVG(HP) AS avg_hp,
       AVG(MP) AS avg_mp
FROM character
GROUP BY job_name
ORDER BY job_name;
```

### 🔹 3NF版

```sql
SELECT j.job_name,
       AVG(c.HP) AS avg_hp,
       AVG(c.MP) AS avg_mp
FROM character c
JOIN job_master j ON c.job_id = j.job_id
GROUP BY j.job_id, j.job_name
ORDER BY j.job_name;
```

### 💬 コメント

- SQLは似ているが結果の信頼性が違う
- 2NF版は job_name そのものがグルーピングキー
  - 表記ゆれが混ざると集計が割れる
- 3NF版は job_id で集計
  - 日本語表示/英語表示/略称に変えても同じグループ

---

## ④ 「存在しない職業を防ぎたい」場合

### 🔹 2NF版

```sql
INSERT INTO character (character_id, person_id, job_name, character_name, HP, MP, EXP)
VALUES (101, 5, 'せんし', 'アルダーン', 150, 80, 1000);
-- 誤字 'せんし' もそのまま登録
```

### 🔹 3NF版

```sql
INSERT INTO character (character_id, person_id, job_id, character_name, HP, MP, EXP)
VALUES (101, 5, 99, 'アルダーン', 150, 80, 1000);
-- job_master に job_id=99 が存在しない場合 FOREIGN KEY エラー
```

### 💬 コメント

- 2NF版は誤字がそのまま保存されデータ汚染
- 3NF版は外部キー制約がデータ品質を守る

---

# 📌 まとめ

| 観点 | 2NF版 | 3NF版 |
|------|-------|-------|
| 更新容易性 | ✗ テーブル横断で複数更新 | ○ 1行更新で完了 |
| 表記ゆれ耐性 | ✗ job_name依存で不安定 | ○ job_id管理で安定 |
| 整合性制約 | ✗ アプリ側で担保 | ○ DB側が担保 |
| 拡張性 | ✗ 手直し増える | ○ 拡張容易 |
| SQL可読性 | ◎ シンプル | ○ JOIN増える |
