#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

# 3.

print("player ID, character ID, character_nane, HP")

cur.execute('select * from character;')
for row in cur:
	comstr = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])
	print(comstr)

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()