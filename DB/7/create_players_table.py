#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

comstr = "create table player (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fname VARCHAR(20), lname VARCHAR(20), points INTEGER, rank VARCHAR(20));"

# 3.�e�[�u���ɐl���f�[�^��o�^����
cur.execute(comstr)

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()