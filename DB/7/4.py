#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

#�f�[�^�x�[�X�ɐڑ�����
conn = sqlite3.connect('TEST.db')
c = conn.cursor()

sql = """DROP TABLE IF EXISTS persons"""

conn.execute(sql)

#�ۑ��i�R�~�b�g�j����
conn.commit()