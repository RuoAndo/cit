#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

# 3.�e�[�u���̃f�[�^���擾
# ��ł́Apersons�e�[�u���f�[�^��S���擾
cur.execute('SELECT * FROM persons')

# �擾�����f�[�^���o��
for row in cur:
    print(row)

# 4.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()