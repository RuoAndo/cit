# -*- coding: Shift-JIS -*-

import time
import random

# ランダム秒待つ(10～30秒の間で待機する)
waitsec=random.randint(1,5)
print(str(waitsec)+"秒後に処理を開始します")
time.sleep(waitsec)
print("処理を開始しました")