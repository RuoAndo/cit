PRAGMA foreign_keys = ON;

-- 既存があれば削除
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS character;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS first_names_ja;
DROP TABLE IF EXISTS last_names_ja;
DROP TABLE IF EXISTS fantasy_names;
DROP TABLE IF EXISTS job_names_tmp;

-- ===== 2NF スキーマ =====

CREATE TABLE player (
  person_id  INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name  TEXT,
  points     INTEGER,
  rank       INTEGER
);

CREATE TABLE character (
  character_id   INTEGER PRIMARY KEY,
  person_id      INTEGER,
  job_name       TEXT,    -- タイポ込みでそのまま保持
  character_name TEXT,
  HP             INTEGER,
  MP             INTEGER,
  EXP            INTEGER,
  FOREIGN KEY (person_id) REFERENCES player(person_id)
);

CREATE TABLE events (
  event_id     INTEGER PRIMARY KEY,
  character_id INTEGER NOT NULL,
  event_type   TEXT,
  event_time   TEXT,
  FOREIGN KEY (character_id) REFERENCES character(character_id)
);

-- 日本人名（名）
CREATE TEMP TABLE first_names_ja (name TEXT);
INSERT INTO first_names_ja (name) VALUES
('太郎'),('花子'),('健太'),('さくら'),('大輔'),
('美咲'),('翔'),('葵'),('悠斗'),('結衣'),
('誠'),('由美'),('直樹'),('恵理'),('拓海'),
('愛'),('陽菜'),('一郎'),('真由'),('悠真'),
('玲奈'),('蓮'),('真央'),('優'),('彩'),
('浩二'),('智子'),('翼'),('あかり'),('和也'),
('奈々'),('亮'),('千尋'),('恭子'),('隼人'),
('真琴'),('郁人'),('茜'),('涼'),('里奈'),
('慎吾'),('香織'),('俊介'),('朋美'),('淳'),
('めぐみ'),('徹'),('裕子'),('勝'),('綾乃');

-- 日本人名（姓）
CREATE TEMP TABLE last_names_ja (name TEXT);
INSERT INTO last_names_ja (name) VALUES
('佐藤'),('鈴木'),('高橋'),('田中'),('伊藤'),
('渡辺'),('山本'),('中村'),('小林'),('加藤'),
('吉田'),('山田'),('佐々木'),('山口'),('斎藤'),
('松本'),('井上'),('木村'),('清水'),('林'),
('山崎'),('阿部'),('森'),('池田'),('橋本'),
('石川'),('山下'),('中島'),('石井'),('小川'),
('前田'),('岡田'),('長谷川'),('藤田'),('後藤'),
('近藤'),('村上'),('遠藤'),('青木'),('藤井'),
('西村'),('福田'),('太田'),('三浦'),('藤原'),
('岡本'),('松田'),('中川'),('中野'),('原田');

-- player に日本名100人
WITH RECURSIVE seq(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 100
)
INSERT INTO player (person_id, first_name, last_name, points, rank)
SELECT
  n AS person_id,
  (SELECT name FROM first_names_ja ORDER BY RANDOM() LIMIT 1),
  (SELECT name FROM last_names_ja  ORDER BY RANDOM() LIMIT 1),
  ABS(RANDOM() % 1000),
  ABS(RANDOM() % 10) + 1
FROM seq;

-- 異世界名候補
CREATE TEMP TABLE fantasy_names (name TEXT);
INSERT INTO fantasy_names (name) VALUES
('アルダーン'),('リュカオン'),('セフィリア'),('ザハル'),
('クレアト'),('アスタリア'),('ヴェルン'),('ナディア'),
('フィオレン'),('ジークハルト'),('ルナティア'),('メルヴィン'),
('アレクシア'),('ドルン'),('オルフェノ'),('サフィール'),
('ゲルダン'),('ティアラ'),('フォルテス'),('レイヴン'),
('ミリアン'),('エルゼ'),('カリオン'),('ノクス'),('イゾルデ'),
('アヴァリス'),('テスラール'),('ベルカイン'),('ロスティア'),
('ヴァルター'),('コーデリア'),('スレイヴ'),('ジルヴァ'),
('フェルナー'),('ラミレス'),('ダンテス'),('ルキウス'),
('アマデラ'),('アリエル'),('タルフォン'),('ガラティア'),
('エルドラン'),('リーシェ'),('クルスフェル'),('オルガ'),
('ベルトラン'),('トリスティア'),('ラグナル'),('オクタヴィア'),('シルファ');

-- 職業名（戦士タイポ含める）を job_id 付きで持つ
CREATE TEMP TABLE job_names_tmp (
  job_id INTEGER PRIMARY KEY,
  name   TEXT
);
INSERT INTO job_names_tmp (job_id, name) VALUES
(0,'戦士'),
(1,'戦士 '),      -- 半角スペース付き
(2,'戦仕'),       -- 誤字
(3,'戦士(剣)'),   -- バリエーション
(4,'せんし'),     -- ひらがな
(5,'魔法使い'),
(6,'僧侶'),
(7,'盗賊'),
(8,'弓使い'),
(9,'格闘家'),
(10,'商人'),
(11,'狩人'),
(12,'賢者'),
(13,'忍者');

-- person_id を 0〜(件数-1) で割った剰余で職業を決める（ここがポイント）
INSERT INTO character (character_id, person_id, job_name, character_name, HP, MP, EXP)
SELECT
  p.person_id,
  p.person_id,
  (
    SELECT name
    FROM job_names_tmp j
    WHERE j.job_id = ((p.person_id - 1) % (SELECT COUNT(*) FROM job_names_tmp))
  ),
  (SELECT name FROM fantasy_names ORDER BY RANDOM() LIMIT 1),
  ABS(RANDOM() % 200) + 100,
  ABS(RANDOM() % 100) + 50,
  ABS(RANDOM() % 5000)
FROM player AS p;

-- events：500件ランダム
WITH RECURSIVE seq2(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM seq2 WHERE n < 500
)
INSERT INTO events (event_id, character_id, event_type, event_time)
SELECT
  n,
  ABS(RANDOM() % 100) + 1,
  CASE ABS(RANDOM() % 3)
    WHEN 0 THEN '戦闘'
    WHEN 1 THEN 'レベルアップ'
    ELSE '休憩'
  END,
  datetime('now', '-' || ABS(RANDOM() % 100000) || ' minutes')
FROM seq2;
