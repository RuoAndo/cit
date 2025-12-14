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
