# -*- coding: Shift-JIS -*-

import time
import random

# �����_���b�҂�(10�`30�b�̊Ԃőҋ@����)
waitsec=random.randint(1,5)
print(str(waitsec)+"�b��ɏ������J�n���܂�")
time.sleep(waitsec)
print("�������J�n���܂���")