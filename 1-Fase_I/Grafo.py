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
            route = nx.shortest_path(self.Grafo, np.random.choice(self.Grafo.nodes), 
                         np.random.choice(self.Grafo.nodes))
            ox.plot_graph_route(self.Grafo, route, fig_height=10, fig_width=10)
#            aux = self.Grafo.nodes[317810430]
#            aux.pop('osmid')
#            aux = tuple(aux.values())
#            self.lib_idx = self.tree.query([aux], return_distance=False)[0]
#            print(self.lib_idx)
#            closest_node_to_lib = self.nodes.iloc[self.lib_idx].index.values[0]
#            print(closest_node_to_lib)
#            ig, ax = ox.plot_graph(self.Grafo, fig_height=10, fig_width=10, 
#                        show=False, close=False, 
#                        edge_color='black')
#            
#            
#            ax.scatter(aux[1], aux[0], c='red', s=100)
#            ax.scatter(self.Grafo.node[closest_node_to_lib]['x'],
#                       self.Grafo.node[closest_node_to_lib]['y'], 
#                       c='green', s=100)
#            print(aux)
#            print(self.Grafo.node[closest_node_to_lib])
#            plt.show()
            

        
        
        def Muestra(self):
            G_projected = ox.project_graph(self.Grafo)
            ox.plot_graph(G_projected)
            