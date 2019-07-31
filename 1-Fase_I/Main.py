# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:15:18 2019
@author: tonibous
"""
import TrackReader as tr
import TrackAnalyzer as ta
import TrackPlot as tp
import TrackSimulator as ts
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from geopy.distance import distance, VincentyDistance
import numpy as np
from operator import itemgetter
import networkx as nx
import geopy.distance
import numpy as np
from geopy import Point
import geopy
import random
import math



parsed_file = tr.load_gpx_file("Rutas/Ficheros/RutaRealCastell4.gpx")
track_points = tr.load_file_points(parsed_file)

track_analyzer = ta.TrackAnalyzer(39.5713,39.5573,2.6257,2.6023)
track_analyzer.set_kdtree()
track_analyzer.get_trackpoint_distance(track_points)


s, m = track_analyzer.viterbi_algorithm(track_points)
i = track_analyzer.get_simplified_route_relation(s)
s = np.array(s)
L = [(x[0],x[1],0) for x in s[:,1]]
L_P = np.array([[x[0],x[1]] for x in s[:,0]])

track_analyzer.analyze_results(s)

ec = ['red' if i in L else 'black' for i in track_analyzer.graph.edges]

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,show=False, close=False, edge_color=ec)


# x = L_P[:,1]
# y = L_P[:,0]
#
# graph, = plt.plot([], [], 'o')
#
# def animate(i):
#     graph.set_data(x[:i+1], y[:i+1])
#     return graph

# ani = animation.FuncAnimation(fig, animate,frames=len(L_P), interval=200)



# tp.plot_points(ax,track_points,'black')
# tp.plot_points(ax,s[:,0],'orange')


# for i in range(0, len(track_points)):
#     ax.plot(track_points[:,0], track_points[:,1], color='black')
# plt.show()

# route = track_analyzer.create_route(s)
# ox.plot_graph_route(track_analyzer.graph, route, fig_height=10, fig_width=10)
#
# for l in L:
#      track_analyzer.update_edge_freq(l[0],l[1])

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------



# track_route_relation = track_analyzer.get_route_relation_from_trackpoint(track_points)
# track_route_relation_filtered = track_analyzer.get_simplified_route_relation(track_route_relation)
#
# originNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,2])
# destinNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,3])
#
# fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,
#             show=False, close=False,
#             edge_color='black')
#
# tp.plot_points(ax, track_points, 'red')
# tp.plot_points(ax, track_route_relation_filtered[:,0:2], 'blue')
#
# tp.plot_points(ax, originNodes, 'orange')
# tp.plot_points(ax,destinNodes, 'orange')
#
# tp.plot_route(track_analyzer.graph,track_route_relation_filtered)
#
# plt.show(block=True)
#
# track_analyzer.get_bearing_point_to_point(track_route_relation_filtered[:,0:2])
# track_analyzer.get_distance_point_to_point(track_route_relation_filtered[:,0:2])
#
# tp.plot_diagrams(track_analyzer.trackpoint_bearing,"Trackpoint Bearing, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_distance,"Trackpoint Distance, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_route_distance,"Route-Track distance, meters",100)

# frecuencies = track_analyzer.getFrequencyRoute(track_route_relation_filtered)
# track_analyzer.setFrequencyToNode(frecuencies)

xxx = [n for i, n in enumerate(L) if i == 0 or n != L[i-1]]
path = []
for x in xxx:
    points = ts.simulate_route(track_analyzer,x[0],x[1])
    path.extend(points)
# tp.plot_points(ax,points,'red')


p = np.array([[a[0],a[1]] for a in path])
x = p[:,1]
y = p[:,0]

graph, = plt.plot([], [], 'o')


def animate(i):
    graph.set_data(x[:i+1], y[:i+1])
    return graph


# ani = animation.FuncAnimation(fig, animate,frames=len(p), interval=200)

tp.plot_points(ax, path, 'red')
plt.show()

