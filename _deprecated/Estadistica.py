#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:35:07 2019

@author: tonibous
"""
from geopy.distance import distance

class Estadistica:
    def __init__(self):
        pass
    
    def obtenerDistancia(puntos):
    distancia=[]
    for p in range(len(puntos)-1):
        distancia.append(distance(puntos[p],puntos[p+1]).m)
    return np.array(distancia)