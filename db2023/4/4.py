#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

for i in range(100000):

	x = random.randint(1, 100)
	y = random.randint(1, 100)

	id = random.randint(101,1000)
	print(id)

	#commstr = "'INSERT INTO XY values(1,3,2)'"
	commstr = "INSERT INTO XY values(" + str(id) + "," + str(x) + "," + str(y) + ");"
	#print(commstr)
	cur.execute(commstr)
	

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()