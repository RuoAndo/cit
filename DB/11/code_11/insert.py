#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

comstr = "insert into player (fname, lname, points, rank) values('taro', 'yamada', '0', 'D');"
cur.execute(comstr)

comstr = "insert into player (fname, lname, points, rank) values('hanako', 'sato', '0', 'D');"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1, 1, 'doraemon', 10, 10, 0);"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(1, 2, 'akinator', 15, 5, 0);"
cur.execute(comstr)

comstr = "insert into character (person_id, character_id, character_name, HP, MP, EXP) values(2, 2, 'akinator', 15, 5, 0);"
cur.execute(comstr)

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()