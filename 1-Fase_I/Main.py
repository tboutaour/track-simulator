#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:15:18 2019

@author: tonibous
"""
import gpxpy
import Grafo as g
import numpy as np
import osmnx as ox


route1 = "RutaCastilloBellver3.gpx"

f1 = open(route1)
p1 = gpxpy.parse(f1)
points_a=[]
points_c=[]
for track in p1.tracks:  # OJO SOLO HAY UN TRACK
    for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
        for iA in range(0, len(segment.points) - 1):
            point = segment.points[iA]
            points_a.append((point.latitude, point.longitude))

    




tolerance = 0.0000009

grafo = g.Grafo(39.5713,39.5573,2.6257,2.6023,p1)
#grafo.Muestra(2)
#grafo.Grafo.edges()
#grafo.GenerarKDtree(0.5)
#grafo.ObtenerPuntoMasCercano()
#grafo.Prueba()

#ejemplo punto cercano:

aux = grafo.Grafo.nodes[np.random.choice(grafo.Grafo.nodes)]
punto = aux
del punto['osmid']
punto = tuple(punto.values())
punto = (39.566531,2.615824)

grafo.GenerarKDtree()

for a in points_a:
    punto_cercano=grafo.ObtenerNodoMasCercano(grafo.nodes,a)
    points_c.append([a,punto_cercano['osmid']])
    

punto_cercano=grafo.ObtenerNodoMasCercano(grafo.nodes,punto)
fig, ax = ox.plot_graph(grafo.Grafo, fig_height=10, fig_width=10, 
            show=False, close=False, 
            edge_color='black')
#ax.scatter(punto[1], punto[0], c='red', s=50)    
ax.scatter(punto_cercano['x'], punto_cercano['y'], c='green', s=50)

#a falta de arreglar porque p_aux es un float object not subscriptable
for a in points_a:
    lat = a[0]
    lon = a[1]
    ax.scatter(lon, lat, c='red', s=20)

for b in points_c:
    lon = grafo.Grafo.node[b[1]]['x']
    lat = grafo.Grafo.node[b[1]]['y']
    ax.scatter(lon, lat, c='blue', s=20)
    
