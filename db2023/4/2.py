#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

x = random.randint(5, 47)
y = random.randint(5, 47)

#commstr = "'INSERT INTO XY values(1,3,2)'"
commstr = "INSERT INTO XY values(1," + str(x) + "," + str(y) + ");"

print(commstr)
cur.execute(commstr)

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()