sqlite3 cit-7.db "drop table person;"

sqlite3 cit-7.db "create table person (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fname VARCHAR(20), lname VARCHAR(20), eye_color CHAR(2), birth_date DATE, street VARCHAR(30), city VARCHAR(20), state VARCHAR(30), country VARCHAR(20), postal_code VARCHAR(20));"

sqlite3 cit-7.db "create table favarite_food (person_id SMALLINT UNSINGED, food varchar(20), constraint pk_favorite_food primary key (person_id, food), constraint fk_fav_food_person_id foreign key (person_id) references person (person_id));"

sqlite3 cit-7.db "insert into person (person_id, fname, lname, eye_color, birth_date) values('1', 'taro', 'yamada', 'BR', '1972-05-27');"

sqlite3 cit-7.db "insert into person (person_id, fname, lname, eye_color, birth_date) values('2', 'hanako', 'sato', 'BR', '1972-10-27');"

sqlite3 cit-7.db "update person set street='minamisenju 17', city='arakawa-ku', state='tokyo', country='japan', postal_code = '1160003' where person_id = 1;"

sqlite3 cit-7.db "insert into favarite_food (person_id, food) values (1, 'pizza');"

sqlite3 cit-7.db "insert into favarite_food (person_id, food) values (1, 'soba');"

sqlite3 cit-7.db "insert into favarite_food (person_id, food) values (2, 'ramen');"

sqlite3 cit-7.db "select p.person_id, p.fname, p.lname, p.birth_date, p.eye_color, p.state, p.city, p.street, favarite_food.food from person p inner join favarite_food on p.person_id = favarite_food.person_id;"