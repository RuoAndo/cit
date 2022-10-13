#%matplotlib nbagg

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import matplotlib.patches as patches

import math

fig, ax = plt.subplots()
ims = []

x = []
y1 = []
y2 = []

for i in range(3000):
    x.append(random.uniform(-1, 1))
    y1.append(random.uniform(-1, 1))
    y2.append(random.uniform(-1, 1))
    
    im = plt.scatter(x,y1,c="red", s=2)
    ims.append([im])
    
    im = plt.scatter(x,y2,c="blue", s=2)
    ims.append([im])
    
ani = animation.ArtistAnimation(fig, ims, interval=5)
plt.show()

#plt.xlabel("X")
#plt.ylabel("Y")
#plt.title("10000/10000")
#plt.show()
