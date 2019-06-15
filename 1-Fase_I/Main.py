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
import networkx as nx
from geopy.distance import distance
import matplotlib.pyplot as plt

def CargaPuntosTrack(fichero):
    points_a=[]
    for track in fichero.tracks:  # OJO SOLO HAY UN TRACK
        for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
            for iA in range(0, len(segment.points) - 1):
                point = segment.points[iA]
                points_a.append([point.latitude, point.longitude])
    return np.array(points_a)

def ObtenerDistancia(puntos):
    distancia=[]
    for p in range(len(puntos)-1):
        distancia.append(distance(puntos[p],puntos[p+1]).m)
    return np.array(distancia)

def GetRouteFromPoint(grafo,data, points_a):
    originNode, destinyNode = grafo.getClosestNodes(data,points_a)
    return np.column_stack((points_a,originNode,destinyNode))

def PlotPoints(ax, t, color):
    for a in t:
        lat = a[0]
        lon = a[1]
        ax.scatter(lon, lat, c= color, s=20)
        
#Función para generar el array bidimensional con todos los puntos y sus nodos or. fin.
def TreeStructureCreation(df):
    roadRelation = df[['source','target','geometry']]
    n = []
    for road in roadRelation.iterrows():
        try:
            coords = road[1].geometry.coords[:]
            coordList = [list(reversed(item)) for item in coords]
            L = [ x + [road[1].source,road[1].target] for x in coordList]
            n.extend(L)
        except AttributeError:
            pass
    return np.array(n)

#...................................................................    
#Método que muestra el cálculo de la distancia. Muestra histograma
#...................................................................
def CalculoDistanciaTrayectorias(n):
    rout ="Rutas/Ficheros/RutaCastilloBellver"
    d=[]
    for i in range(n):
        rout ="Rutas/Ficheros/RutaCastilloBellver"
        rout=rout+str(i+1)+".gpx"
        f1 = open(rout)
        p1 = gpxpy.parse(f1)
        points_a=[]
        for track in p1.tracks:  # OJO SOLO HAY UN TRACK
            for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
                for iA in range(0, len(segment.points) - 1):
                    point = segment.points[iA]
                    points_a.append((point.latitude, point.longitude))
        for p in range(len(points_a)-1):
            d.append(distance(points_a[p],points_a[p+1]).m)
        
    plt.hist(d, bins=70)
    
    plt.xlabel('distance')
    plt.show()  

#...................................................................    
#Primer Main.
#Genera a partir de un fichero todo el grafo y una comparación con una ruta
#...................................................................

route1 = "Rutas/Ficheros/castillo-bellver.gpx"
f1 = open(route1)
p1 = gpxpy.parse(f1)

points_c=[]

puntos_track = CargaPuntosTrack(p1)

distancia = ObtenerDistancia(puntos_track)

simulador = g.Grafo(39.5713,39.5573,2.6257,2.6023,p1)
simulador.Grafo = simulador.Grafo.to_undirected()

df=nx.to_pandas_edgelist(simulador.Grafo)
data = TreeStructureCreation(df)
simulador.GenerarKDtreeSegmentos(data)

trackRouteRelation = GetRouteFromPoint(simulador,data,puntos_track)

fig, ax = ox.plot_graph(simulador.Grafo, fig_height=10, fig_width=10, 
            show=False, close=False, 
            edge_color='black')

PlotPoints(ax, puntos_track, 'red')
originNodes = simulador.GetNodePoints(trackRouteRelation[:,2])
destinNodes = simulador.GetNodePoints(trackRouteRelation[:,3])
PlotPoints(ax, originNodes, 'green')
PlotPoints(ax,destinNodes, 'green')

