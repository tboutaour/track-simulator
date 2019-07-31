# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import pandas as pd
from geopy.distance import distance, VincentyDistance
import geopy.distance
import numpy as np
from geopy import Point
import geopy
import random
import math
import TrackAnalyzer as ta
import networkx as nx

from geopy.distance import distance, VincentyDistance


def get_random_value(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))


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


def getPoint(la1, lo1, b, d):
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

    print("lat " + str(lat2))
    print("lon " + str(lon2))
    return (lat2, lon2)


def simulate_segment(ta, seg):
    """
    Simulate creation of points in the segment delimited by two nodes of the graph
    :param self:
    :param ta: TrackAnalysis of the project with all the information for recreating the segment
    :param seg: Segment to simulate (Origin node, Target node)
    :return: Array of points (lat,lon) of the simulation
    """
    gen_points_number = get_random_value(ta.trackpoint_number)
    origin_node = seg[0]
    target_node = seg[1]
    segment = []
    origin_point = Point(ta.graph.nodes[origin_node]['y'], ta.graph.nodes[origin_node]['x'])
    target_point = Point(ta.graph.nodes[target_node]['y'], ta.graph.nodes[target_node]['x'])
    d = geopy.distance.distance(origin_point, target_point).m
    try:
        coords = ta.graph.edges[(origin_node, target_node, 0)]['geometry'].coords[:]
        coord_list = [list(reversed(item)) for item in coords]


        dest, aux = calculate_point(ta, segment, coord_list, origin_node, target_node, origin_point, target_point)
        next = dest

        while aux > 12 and aux < d * 1.5 and len(segment) < gen_points_number:
            dest, aux = calculate_point(ta, segment, coord_list, origin_node, target_node, next, target_point)
            next = dest

    except KeyError:
        pass

    return np.array(segment)


#revisar
def calculate_point(ta,segment, coord_list, origin_node, target_node, origin_point, target_point):
    #Coger el nodo más cercano
    idx = get_closest_segment_point(ta, coord_list, origin_node, target_node, origin_point)
    print("indiiiceeee --------------- : "+str(idx))
    #Apuntaremos n nodos a partir del más cercano
    try:
        bearing = calculate_initial_compass_bearing((origin_point[0], origin_point[1]), (coord_list[idx+5][0], coord_list[idx+5][1]))
    except IndexError:
        print("Ha habido un error:::::::::::::::")
        print(origin_node)
        print(target_node)
        #Si nos hemos pasado con el indice apuntaremos al final.
        bearing = calculate_initial_compass_bearing((origin_point[0], origin_point[1]), (target_point[0],target_point[1]))

    rndbear = random.uniform(bearing - 10, bearing + 10)
    # point_distance = get_random_value(ta.trackpoint_distance)/8000
    point_distance = 0.01
    dest = getPoint(origin_point[0], origin_point[1], rndbear, point_distance)
    aux = geopy.distance.distance(dest, target_point).m

    # Meter el punto en el segmento resultante
    segment.append(Point(dest[0], dest[1]))
    return dest, aux

def get_closest_segment_point(ta, coord_list, origin_node, target_node, point):

    a, b = ta.get_closest_nodes([[point[0], point[1]]], 0.001)
    aux = []
    for idx in range(0,len(a)):
        aux.append([a[idx][0],a[idx][1],b[0][idx]])

    aux = sorted(aux, key=lambda x : x[2])
    correct_aux = [a for a in aux if a[1] == (origin_node, target_node)]
    print("PA: "+str(correct_aux[0][0][0]))
    print("PB: "+str(correct_aux[0][0][1]))
    print("Dstc: "+str(correct_aux[0][2]))
    try:
        idx = coord_list.index([correct_aux[-1][0][0], correct_aux[-1][0][1]])
    except ValueError:
        idx = len(coord_list)
    return idx


def simulate_route(ta, origin, end):
    track = []
    # Simular creación de trayectoria completa
    # Encontrar el camino Dijsktra desde un nodo inicio seleccionado al final.
    dijkstra = nx.dijkstra_path(ta.graph, origin, end, 'frequency')
    path = []
    for d in range(0,len(dijkstra)-1):
        path.append([dijkstra[d],dijkstra[d+1]])
    # Iterar para cada uno de los nodos del camino escogido
    for segment in path:
        print("Segmento:::::"+str(segment))
        seg = simulate_segment(ta, segment)
        for s in seg:
            print("seg....: " + str(s))
            track.append(s)
    return np.array(track)

