#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('SELECT * FROM XY')

# �擾�����f�[�^���o��
for row in cur:
    print(row)

# 4.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()