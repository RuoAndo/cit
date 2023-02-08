#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

comstr = "insert into player (fname, lname, points, rank) values('taro', 'yamada', '0', 'D');"
cur.execute(comstr)

comstr = "insert into player (fname, lname, points, rank) values('hanako', 'sato', '0', 'D');"
cur.execute(comstr)

for i in range(100):


	tmp = 100 + random.randint(0, 50)

	print(i)
	comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1," + str(i) + ",'doraemon'," + str(tmp) + ",50, 0);"
	cur.execute(comstr)

	tmp = 150 + random.randint(0, 50)

	comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1," + str(i) + ",'akinator'," + str(tmp) + ",75, 0);"
	cur.execute(comstr)

	tmp = 200 + random.randint(0, 50)

	comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(2," + str(i) + ",'akinator'," + str(tmp) + ",25, 0);"
	cur.execute(comstr)

comstr2 = "create table events (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), event_type VARCHAR(20), event_time VARCHAR(20), event_counter INTEGER);"

now = datetime.datetime.now()
print(now)

#####

#comstr2 = "create table events (person_id INTEGER, character_id INTEGER, character_name VARCHAR(20), event_type VARCHAR(20), event_time VARCHAR(20), event_counter INTEGER);"

comstr = "insert into events (person_id, character_id, character_name, event_type, event_time, event_counter, HP) values(1, 1, 'doraemon', 'create'," + "'" + str(now) + "'" + ", 1, 0);"
cur.execute(comstr)

comstr = "insert into events (person_id, character_id, character_name, event_type, event_time, event_counter, HP) values(1, 2, 'akinator', 'create'," + "'" + str(now) + "'" + ", 2, 0);"
cur.execute(comstr)

comstr = "insert into events (person_id, character_id, character_name, event_type, event_time, event_counter, HP) values(2, 2, 'akinator', 'create'," + "'" + str(now) + "'" + ", 3, 0);"
cur.execute(comstr)

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

cur = conn.cursor()
cur.execute('select * from character')

for row in cur:
	print(row)


# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()