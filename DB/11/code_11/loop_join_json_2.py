#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random
import time

import json

dbname = 'cit-7.db'
# 1.�f�[�^�x�[�X�ɐڑ�
conn = sqlite3.connect(dbname)

i = 0

while i < 500:

	# 2.sqlite�𑀍삷��J�[�\���I�u�W�F�N�g���쐬
	cur = conn.cursor()
	
	#cur.execute('.mode json')
	cur.execute('select * from player inner join character on character.person_id = player.person_id;')

	#(1, 'taro', 'yamada', 0, 'D', 1, 1, 'doraemon', -267, 10, 0)
	#(1, 'taro', 'yamada', 0, 'D', 1, 2, 'akinator', -289, 5, 0)
	#(2, 'hanako', 'sato', 0, 'D', 2, 2, 'akinator', -289, 5, 0)

	list1 = []

	for row in cur:
		d = {}
		list2 = []
		print(row)

		for i in row:
			print(i)

		#list1.append(list2)
	
	print(list1)
	
	print("-----")
	
	time.sleep(2)
    
# 5.�f�[�^�x�[�X�̐ڑ���ؒf
cur.close()
conn.close()

