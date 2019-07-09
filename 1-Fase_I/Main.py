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
from geopy.distance import distance, VincentyDistance
import numpy as np
from geopy import Point
from operator import itemgetter
import networkx as nx
import geopy.distance
import numpy as np
from geopy import Point
import geopy
import random
import math


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

# tp.plot_diagrams(track_analyzer.trackpoint_bearing,"Trackpoint Bearing, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_distance,"Trackpoint Distance, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_route_distance,"Route-Track distance, meters",100)

frecuencies = track_analyzer.getFrequencyRoute(track_route_relation_filtered)
track_analyzer.setFrequencyToNode(frecuencies)

def simularPuntos(punto,ax):
    PuntoOrigen = punto
    for i in range(0,5):
        distanceRandomPointPoint = ts.GetRandomValue(track_analyzer.trackpoint_distance)
        bearingRandomValue = ts.GetRandomValue(track_analyzer.trackpoint_bearing)
        point = VincentyDistance(meters=25).destination(Point(PuntoOrigen[0],
                                                                                    PuntoOrigen[1]),
                                                                              bearingRandomValue)
        tp.plot_points(ax,[np.array([point[0],point[1]])],'black')
        PuntoOrigen = point

# fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,
#             show=False, close=False,
#             edge_color='black')
# simularPuntos(Point(track_route_relation_filtered[40][0], track_route_relation_filtered[40][1]),ax)
# plt.show()



red_edges = [(304661508, 699940277,0)]
pos = nx.spring_layout(track_analyzer.graph)
# nx.draw_networkx_nodes(track_analyzer.graph,pos,node_size = 20)
# nx.draw_networkx_labels(track_analyzer.graph,pos)
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def getPoint(la1,lo1,b,d):
    R = 6378.1  # Radius of the Earth
    brng = math.radians(b)  # Bearing is 90 degrees converted to radians.
    # d = 0.1  # Distance in km

    # lat2  52.20444 - the lat result I'm hoping for
    # lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(la1)  # Current lat point converted to radians
    lon1 = math.radians(lo1)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print("lat "+str(lat2))
    print("lon "+str(lon2))
    return (lat2,lon2)

def prueba(grafo,ax,paramd,perim,col,p1,p2):
    start = Point(track_analyzer.graph.node[p1]['y'],track_analyzer.graph.node[p1]['x'])
    end = Point(track_analyzer.graph.node[p2]['y'],track_analyzer.graph.node[p2]['x'])
    d = geopy.distance.distance(start,end).m
    # print("distancia start-end: "+str(d))
    bearing = calculate_initial_compass_bearing((start[0],start[1]),(end[0],end[1]))
    # print("bearing start-end : " + str(bearing))
    rndbear=random.uniform(bearing-60,bearing+60)
    # print("rndbearing : "+str(rndbear))
    dest = getPoint(start[0],start[1],rndbear,paramd)
    # ax.scatter(dest[0], dest[1], c='green')
    tp.plot_points(ax, [np.array([dest[0], dest[1]])], col)
    # ax.plot([start[0], dest[0]], [start[1], dest[1]], c='blue')
    aux = geopy.distance.distance(dest, end).m
    # print("distancia actual:"+str(aux))
    next = dest
    while aux > perim and aux < d*1.5:
        rndbear = random.uniform(bearing - 45, bearing + 45)
        # print("rndbearing : " + str(rndbear))
        dest = getPoint(next[0], next[1], rndbear, paramd)
        ax.scatter(dest[0], dest[1], c='green')
        tp.plot_points(ax, [np.array([dest[0], dest[1]])], col)
        # ax.plot([next[0],dest[0]],[next[1],dest[1]],c='blue')
        next = dest
        # print("distancia actual:" + str(aux))
        aux = geopy.distance.distance(dest, end).m
    # dest = (d.destination(point = start, bearing=45))
    # print(dest)
    d = geopy.distance.distance(start, dest).m
    # print("distancia start-dest: "+str(d))

start = Point(track_analyzer.graph.node[304661508]['y'], track_analyzer.graph.node[304661508]['x'])
end = Point(track_analyzer.graph.node[304661509]['y'], track_analyzer.graph.node[304661509]['x'])

fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,
            show=False, close=False)
lista = [[a,b] for (a,b,c) in track_analyzer.graph.edges]
for i in lista:
    p1 = i[0]
    p2 = i[1]
    # ec = ['red' if i == (304661508, 699940277,0) else 'black' for i in track_analyzer.graph.edges]
    # nc = ['red' if (i == p1 or i ==p2) else 'black' for i in track_analyzer.graph.nodes]

    nx.draw_networkx_edges(track_analyzer.graph,pos,edgelist=red_edges,edge_color='red')
    color = ['blue','green','purple','orange']
    for i in range(0,4):
        # ax3 = plt.subplot()
        # ax3.margins(x=-0.2,y=-0.2)   # Values in (-0.5, 0.0) zooms in to center
        # ax3.scatter(start[0],start[1],c='red')
        # ax3.scatter(end[0],end[1],c='red')
        # ax3.plot([start[0],end[0]],[start[1],end[1]],c='black')
        # ax3.set_title('Zoomed in')
        prueba(track_analyzer.graph,ax,0.02,25,color[i],p1,p2)
plt.show()


