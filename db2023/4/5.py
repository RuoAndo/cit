#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

cur = conn.cursor()

start = time.time()  
cur.execute('SELECT * FROM XY')
end = time.time()  

# �擾�����f�[�^���o��
#for row in cur:
#    print(row)

time_diff = end - start  # ����������̎������珈���J�n�O�̎��������Z����
print(time_diff)  # �����ɂ����������ԃf�[�^���g�p

# 4.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()