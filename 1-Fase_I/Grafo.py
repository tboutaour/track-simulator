#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:01:48 2019

@author: tonibous
"""

import osmnx as ox
from sklearn.neighbors import KDTree
import scipy.spatial
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.neighbors import KDTree
import folium
import gpxpy

class Grafo:
        def __init__(self, north, south,east,west,p1):
            self.north = north
            self.south = south
            self.east = east
            self.west = west
            self.Grafo = ox.graph_from_bbox(self.north,self.south,self.east,self.west)
            self.p1 = p1
            
        def __colorear_rutas(self):
            return ox.get_edge_colors_by_attr(self.Grafo, attr='length')
            
        def GenerarKDtree(self):
            self.nodes, _ = ox.graph_to_gdfs(self.Grafo)
            self.tree = KDTree(self.nodes[['y', 'x']], metric='euclidean')

        def Muestra(self,n):
            G_projected = ox.project_graph(self.Grafo)
            if n == 2:
                fig, ax = ox.plot_graph(self.Grafo,show=False, close=False, edge_color=(self.__colorear_rutas()))
            else:
                fig, ax = ox.plot_graph(G_projected,show=False, close=False, )
            aux = self.__ImprimirSegmentoRuta("CastilloBellver.gpx")
            ax = ax.scatter(aux[1], aux[0], c='red', s=20)
            
        def GenerarRutaRandom(self):
            route = nx.shortest_path(self.Grafo, np.random.choice(self.Grafo.nodes), 
            np.random.choice(self.Grafo.nodes))
            ox.plot_graph_route(self.Grafo, route, fig_height=10, fig_width=10)
        
        def GenerarPuntoRandom(self):
            aux = self.Grafo.nodes[np.random.choice(self.Grafo.nodes)]
            fig, ax = ox.plot_graph(self.Grafo, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
            ax.scatter(aux['x'], aux['y'], c='red', s=100)
            
        def ObtenerNodoMasCercano(self,nodos,punto):
            idx_cerc = self.tree.query([punto], k=1, return_distance=False)[0]
            punt_cerc = self.Grafo.node[(self.nodes.iloc[idx_cerc].index.values[0])]
            
            return punt_cerc
            
            
        def __CargarPuntos(self, p):
            points_a = []
            #p.simplify()
            #p.reduce_points(500)
            for track in p.tracks:  # OJO SOLO HAY UN TRACK
                for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
                    for iA in range(0, len(segment.points) - 1):
                        point = segment.points[iA]
                        points_a.append([point.longitude, point.latitude])
            return np.asarray(points_a)
        
        def colorear_rutas(self):
            return ox.get_edge_colors_by_attr(self.Grafo, attr='length')
            
        def __ImprimirSegmentoRuta(self,route):
            gpx_file = open(route, 'r')
            gpx = gpxpy.parse(gpx_file)
            lon=[]
            lat=[]
            track = gpx.tracks[0]

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)
            coor =[lat,lon] 
            return coor


        def Prueba(self):
            puntos = np.vstack(self.__CargarPuntos(self.p1))
            print(puntos)
            all_points = [puntos]
            print(all_points)
            all_pts = np.vstack([np.hstack([a, 0])
                                  for a in puntos])
            print(all_pts)
            points_within_tolerance = self.tree.query_ball_point(puntos, 0.0000009)
            print(points_within_tolerance)
            vfunc = np.vectorize(lambda a: np.any( ))
            self.matches = vfunc(points_within_tolerance)
        

            