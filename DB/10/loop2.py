#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

i = 0

while i < 500:

	# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
	cur = conn.cursor()

	# 3.

	print("[before]")
	print("player ID, character ID, character_nane, HP")

	cur.execute('select * from character;')

	for row in cur:

		cur2 = conn.cursor()

		print(row)
		strhp = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3])
		#print(strhp)

		charaID = row[1];
		damage = random.randint(0, 5)	
		currentHP = row[3]
		nextHP = currentHP - damage

		comstr = "update character set HP=" + str(nextHP) + " where character_id = " + str(charaID) + ";"
		#print(comstr)
		cur2.execute(comstr)

		cur2.close()
	
	conn.commit()

	print("---")
	print("[after]")
	print("player ID, character ID, character_nane, HP")

	cur.execute('select * from character;')
	for row in cur:
		print(row)
    
	time.sleep(3)
    
# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()

