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

parsed_file = tr.load_gpx_file("Rutas/Ficheros/RutaRealCastell3.gpx")
track_points = tr.load_file_points(parsed_file)

track_analyzer = ta.TrackAnalyzer(39.5713,39.5573,2.6257,2.6023)
track_analyzer.set_kdtree()
track_analyzer.get_trackpoint_distance(track_points)

track_route_relation = track_analyzer.get_route_relation_from_trackpoint(track_points)
track_route_relation_filtered = track_analyzer.get_simplified_route_relation(track_route_relation)

originNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,2])
destinNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,3])

fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,
            show=False, close=False,
            edge_color='black')

tp.plot_points(ax, track_points, 'red')
tp.plot_points(ax, track_route_relation_filtered[:,0:2], 'blue')

tp.plot_points(ax, originNodes, 'orange')
tp.plot_points(ax,destinNodes, 'orange')

tp.plot_route(track_analyzer.graph,track_route_relation_filtered)

plt.show(block=True)

track_analyzer.get_bearing_point_to_point(track_route_relation_filtered[:,0:2])
track_analyzer.get_distance_point_to_point(track_route_relation_filtered[:,0:2])

tp.plot_diagrams(track_analyzer.trackpoint_bearing,"Trackpoint Bearing, meters",100)
tp.plot_diagrams(track_analyzer.trackpoint_distance,"Trackpoint Distance, meters",100)
tp.plot_diagrams(track_analyzer.trackpoint_route_distance,"Route-Track distance, meters",100)


