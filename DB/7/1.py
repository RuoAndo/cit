#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

# 3.�e�[�u����Create�������s(��ł�persons�e�[�u�����쐬)
cur.execute(
    'CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')

# 4.�f�[�^�x�[�X�ɏ����R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()