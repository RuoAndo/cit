#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TEST.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
cur = conn.cursor()

# 3.�e�[�u���ɐl���f�[�^��o�^����
# ��ł́Apersons�e�[�u����name�J�����ɁuSato�v�uSuzuki�v�uTakahashi�v�Ƃ����f�[�^��o�^
cur.execute('INSERT INTO persons(name) values("Sato")')

cur.execute('INSERT INTO persons(name) values("Suzuki")')

cur.execute('INSERT INTO persons(name) values("Takahashi")')

# 4.�f�[�^�x�[�X�Ƀf�[�^���R�~�b�g
conn.commit()

# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()


