import matplotlib.pyplot as plt
import numpy as np
from geopy import Point
import geopy
import geopy.distance
import random


plt.scatter(3, 9, s=20)
plt.scatter(6, 9, s=20)
plt.plot([3,6],[9,9])
start = geopy.Point(3,9)




# d = geopy.distance.VincentyDistance(kilometers=10)
# rnd = random.randint(0,0)
# print(rnd)
# dest = (d.destination(point = start, bearing=180))
# plt.scatter(dest[0], dest[1])

plt.show()