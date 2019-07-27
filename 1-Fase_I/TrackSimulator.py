# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import numpy as np
import pandas as pd
from geopy.distance import distance, VincentyDistance

def GetRandomValue(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))
