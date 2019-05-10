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


route1 = "RutaCastilloBellver1.gpx"

f1 = open(route1)
p1 = gpxpy.parse(f1)

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

grafo.GenerarKDtree()
punto_cercano=grafo.ObtenerNodoMasCercano(grafo.nodes,punto)
fig, ax = ox.plot_graph(grafo.Grafo, fig_height=10, fig_width=10, 
            show=False, close=False, 
            edge_color='black')
ax.scatter(punto[1], punto[0], c='red', s=50)
ax.scatter(punto_cercano['x'], punto_cercano['y'], c='green', s=50)