#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:01:48 2019

@author: tonibous
"""

import osmnx as ox
from sklearn.neighbors import KDTree
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.neighbors import KDTree
import folium

class Grafo:
        def __init__(self, north, south,east,west):
            self.north = north
            self.south = south
            self.east = east
            self.west = west
            self.Grafo = ox.graph_from_bbox(self.north,self.south,self.east,self.west)
        
        def GenerarKDtree(self,tolerance):
            self.nodes, _ = ox.graph_to_gdfs(self.Grafo)
            self.nodes.head()
            self.tree = KDTree(self.nodes[['x','y']])

        def Muestra(self):
            G_projected = ox.project_graph(self.Grafo)
            ox.plot_graph(G_projected)
            
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
        
        def ObtenerPuntoMasCercano(self):
            nodes, _ = ox.graph_to_gdfs(self.Grafo)
            tree = KDTree(nodes[['y', 'x']], metric='euclidean')
            aux = self.Grafo.nodes[np.random.choice(self.Grafo.nodes)]
            aux1 = aux
            del aux1['osmid']
            aux1 = tuple(aux1.values())
            idx_cerc = tree.query([aux1], k=2, return_distance=False)[0]
            punt_cerc = self.Grafo.node[(nodes.iloc[idx_cerc].index.values[1])]
            fig, ax = ox.plot_graph(self.Grafo, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
            ax.scatter(aux['x'], aux['y'], c='red', s=50)
            ax.scatter(punt_cerc['x'], punt_cerc['y'], c='green', s=50)