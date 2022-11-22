sqlite3 cit-7.db "drop table player;"
sqlite3 cit-7.db "drop table character;"

sqlite3 cit-7.db "create table player (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));"

sqlite3 cit-7.db "create table character (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), HP INTERGER, MP INTEGER, EXP INTEGER);"

sqlite3 cit-7.db "insert into player (fname, lname, points, rank) values('taro', 'yamada', '0', 'D');"
sqlite3 cit-7.db "insert into player (fname, lname, points, rank) values('hanako', 'sato', '0', 'D');"  

sqlite3 cit-7.db "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1, 1, 'doraemon', 10, 10, 0);"
sqlite3 cit-7.db "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(2, 2, 'akinator', 15, 5, 0);"