# 正規化前（第１正規形）

<pre>
1.
PS D:\cit\db2025\10> cp ..\sqlite3.exe .

2.
PS D:\cit\db2025\10> .\sqlite3.exe game_1.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.

3.
sqlite> CREATE TABLE players (player_id INTEGER PRIMARY KEY, player_name TEXT NOT NULL UNIQUE, country TEXT, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP));

4.
sqlite> CREATE TABLE characters (character_id INTEGER PRIMARY KEY, player_id INTEGER NOT NULL, character_name TEXT NOT NULL, class TEXT NOT NULL, rarity INTEGER NOT NULL, level INTEGER NOT NULL DEFAULT 1, hp INTEGER NOT NULL, atk INTEGER NOT NULL, def INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP), FOREIGN KEY (player_id) REFERENCES players(player_id));

5.
sqlite> CREATE INDEX idx_characters_player_id ON characters(player_id);

6.
sqlite> INSERT INTO players (player_id, player_name, country) VALUES (1,'Aki','JP'),(2,'Mina','JP'),(3,'Ren','JP'),(4,'Sora','JP');

7.
sqlite> INSERT INTO characters (character_id, player_id, character_name, class, rarity, level, hp, atk, def) VALUES (1,1,'Kurogane','Warrior',4,18,820,120,80),(2,1,'Mizuki','Mage',3,14,540,160,40),(3,2,'Hibana','Rogue',5,22,610,210,55),(4,2,'Tsubasa','Healer',2,11,680,60,65),(5,3,'Ginga','Archer',4,19,590,175,50),(6,3,'Oboro','Tank',3,16,980,95,120),(7,4,'Kasumi','Mage',5,24,560,240,45),(8,4,'Raiden','Warrior',2,10,760,85,70);

8.
sqlite> .tables
characters  players

9.
sqlite> SELECT p.player_name, COUNT(*) AS char_count FROM players p JOIN characters c ON c.player_id = p.player_id GROUP BY p.player_id ORDER BY char_count DESC, p.player_name LIMIT 5;
Aki|2
Mina|2
Ren|2
Sora|2

10.
sqlite> SELECT character_name, class, rarity, level, hp, atk, def FROM characters ORDER BY atk DESC, rarity DESC, level DESC;
Kasumi|Mage|5|24|560|240|45
Hibana|Rogue|5|22|610|210|55
Ginga|Archer|4|19|590|175|50
Mizuki|Mage|3|14|540|160|40
Kurogane|Warrior|4|18|820|120|80
Oboro|Tank|3|16|980|95|120
Raiden|Warrior|2|10|760|85|70
Tsubasa|Healer|2|11|680|60|65

11.
sqlite> SELECT p.player_name, c.character_name, c.class, c.rarity, c.level FROM players p JOIN characters c ON c.player_id = p.player_id WHERE p.player_name='Sora' ORDER BY c.rarity DESC, c.level DESC LIMIT 5;
Sora|Kasumi|Mage|5|24
Sora|Raiden|Warrior|2|10
</pre>

# 正規化（第３正規形）

<pre>
1. players
プレイヤー情報（4人）

2. characters
キャラクター本体（8体、プレイヤーに従属）

3. classes
職業マスタ（Warrior / Mage など）

4. rarities
レア度マスタ（1〜5段階）

① players（プレイヤー）
CREATE TABLE players (player_id INTEGER PRIMARY KEY, player_name TEXT NOT NULL UNIQUE, country TEXT, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP));

INSERT INTO players (player_id, player_name, country) VALUES (1,'Aki','JP'),(2,'Mina','JP'),(3,'Ren','JP'),(4,'Sora','JP');

② classes（職業マスタ）
CREATE TABLE classes (class_id INTEGER PRIMARY KEY, class_name TEXT NOT NULL UNIQUE, role TEXT NOT NULL);

INSERT INTO classes (class_id, class_name, role) VALUES (1,'Warrior','Melee'),(2,'Mage','Magic'),(3,'Rogue','DPS'),(4,'Healer','Support'),(5,'Archer','Ranged'),(6,'Tank','Defense');

③ rarities（レア度マスタ）
CREATE TABLE rarities (rarity_id INTEGER PRIMARY KEY, rarity_level INTEGER NOT NULL UNIQUE, label TEXT NOT NULL);

INSERT INTO rarities (rarity_id, rarity_level, label) VALUES (1,1,'Common'),(2,2,'Uncommon'),(3,3,'Rare'),(4,4,'Epic'),(5,5,'Legendary');

④ characters（キャラクター本体）
CREATE TABLE characters (character_id INTEGER PRIMARY KEY, player_id INTEGER NOT NULL, character_name TEXT NOT NULL, class_id INTEGER NOT NULL, rarity_id INTEGER NOT NULL, level INTEGER NOT NULL DEFAULT 1, hp INTEGER NOT NULL, atk INTEGER NOT NULL, def INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP), FOREIGN KEY (player_id) REFERENCES players(player_id), FOREIGN KEY (class_id) REFERENCES classes(class_id), FOREIGN KEY (rarity_id) REFERENCES rarities(rarity_id));

INSERT INTO characters (character_id, player_id, character_name, class_id, rarity_id, level, hp, atk, def) VALUES (1,1,'Kurogane',1,4,18,820,120,80),(2,1,'Mizuki',2,3,14,540,160,40),(3,2,'Hibana',3,5,22,610,210,55),(4,2,'Tsubasa',4,2,11,680,60,65),(5,3,'Ginga',5,4,19,590,175,50),(6,3,'Oboro',6,3,16,980,95,120),(7,4,'Kasumi',2,5,24,560,240,45),(8,4,'Raiden',1,2,10,760,85,70);

確認

SELECT p.player_name, c.character_name, cl.class_name, r.rarity_level FROM characters c JOIN players p ON c.player_id=p.player_id JOIN classes cl ON c.class_id=cl.class_id JOIN rarities r ON c.rarity_id=r.rarity_id ORDER BY p.player_id, c.character_id;

PS D:\cit\db2025> .\sqlite3.exe game_3.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.

sqlite> CREATE TABLE players (player_id INTEGER PRIMARY KEY, player_name TEXT NOT NULL UNIQUE, country TEXT, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP));

sqlite> INSERT INTO players (player_id, player_name, country) VALUES (1,'Aki','JP'),(2,'Mina','JP'),(3,'Ren','JP'),(4,'Sora','JP');

sqlite> CREATE TABLE classes (class_id INTEGER PRIMARY KEY, class_name TEXT NOT NULL UNIQUE, role TEXT NOT NULL);

sqlite> INSERT INTO classes (class_id, class_name, role) VALUES (1,'Warrior','Melee'),(2,'Mage','Magic'),(3,'Rogue','DPS'),(4,'Healer','Support'),(5,'Archer','Ranged'),(6,'Tank','Defense');

sqlite> CREATE TABLE rarities (rarity_id INTEGER PRIMARY KEY, rarity_level INTEGER NOT NULL UNIQUE, label TEXT NOT NULL);

sqlite> INSERT INTO rarities (rarity_id, rarity_level, label) VALUES (1,1,'Common'),(2,2,'Uncommon'),(3,3,'Rare'),(4,4,'Epic'),(5,5,'Legendary');

sqlite> CREATE TABLE characters (character_id INTEGER PRIMARY KEY, player_id INTEGER NOT NULL, character_name TEXT NOT NULL, class_id INTEGER NOT NULL, rarity_id INTEGER NOT NULL, level INTEGER NOT NULL DEFAULT 1, hp INTEGER NOT NULL, atk INTEGER NOT NULL, def INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP), FOREIGN KEY (player_id) REFERENCES players(player_id), FOREIGN KEY (class_id) REFERENCES classes(class_id), FOREIGN KEY (rarity_id) REFERENCES rarities(rarity_id));

sqlite> INSERT INTO characters (character_id, player_id, character_name, class_id, rarity_id, level, hp, atk, def) VALUES (1,1,'Kurogane',1,4,18,820,120,80),(2,1,'Mizuki',2,3,14,540,160,40),(3,2,'Hibana',3,5,22,610,210,55),(4,2,'Tsubasa',4,2,11,680,60,65),(5,3,'Ginga',5,4,19,590,175,50),(6,3,'Oboro',6,3,16,980,95,120),(7,4,'Kasumi',2,5,24,560,240,45),(8,4,'Raiden',1,2,10,760,85,70);

sqlite> SELECT p.player_name, c.character_name, cl.class_name, r.rarity_level FROM characters c JOIN players p ON c.player_id=p.player_id JOIN classes cl ON c.class_id=cl.class_id JOIN rarities r ON c.rarity_id=r.rarity_id ORDER BY p.player_id, c.character_id;
Aki|Kurogane|Warrior|4
Aki|Mizuki|Mage|3
Mina|Hibana|Rogue|5
Mina|Tsubasa|Healer|2
Ren|Ginga|Archer|4
Ren|Oboro|Tank|3
Sora|Kasumi|Mage|5
Sora|Raiden|Warrior|2

</pre>
