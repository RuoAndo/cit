#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

HP = random.randint(0, 20)
MP = random.randint(0, 20)
comstr = "update character set HP=" + str(HP) + ", MP=" + str(MP) + ", EXP=5 where character_id = 1;"

# 3.�e�[�u���ɐl���f�[�^��o�^����
cur.execute(comstr)

HP = random.randint(0, 20)
MP = random.randint(0, 20)
comstr = "update character set HP=" + str(HP) + ", MP=" + str(MP) + ", EXP=5 where character_id = 2;"

cur.execute(comstr)


# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()