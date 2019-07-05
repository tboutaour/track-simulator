# -*- coding: utf-8 -*-
"""
@author: tonibous
"""

import osmnx as ox
from sklearn.neighbors import KDTree
import numpy as np
import pandas as pd
from geopy.distance import distance, VincentyDistance
import networkx as nx
import math

class TrackAnalyzer:
    def __init__(self,north, south,east,west):
        self.graph = ox.graph_from_bbox(north,south,east,west).to_undirected()
        self.df = nx.to_pandas_edgelist(self.graph)
        self.trackpoint_distance = []
        self.trackpoint_route_distance = []
        self.trackpoint_bearing = []
        self.route_data = []
        self.__tree = -1

    def get_trackpoint_distance(self,track_points):
        for p in range(len(track_points) - 1):
            self.trackpoint_distance.append(distance(track_points[p], track_points[p + 1]).m)

    # Función para generar el array bidimensional con todos los puntos DE LA RUTA y sus nodos or. fin.
    def create_tree_structure(self):
        roadRelation = self.df[['source', 'target', 'geometry']]
        n = []
        for road in roadRelation.iterrows():
            try:
                coords = road[1].geometry.coords[:]
                coordList = [list(reversed(item)) for item in coords]
                L = [x + [road[1].source, road[1].target] for x in coordList]
                n.extend(L)
            except AttributeError:
                pass
        return np.array(n)

    def set_kdtree(self):
        self.route_data = self.create_tree_structure()
        self.__tree = KDTree(self.route_data[:, :2], metric='euclidean')

    def get_closest_node(self,puntos):
        dist_cerc, idx_cerc = self.__tree.query(puntos, k = 1 , return_distance=True)
        return self.route_data[idx_cerc[:,0]][:,2], self.route_data[idx_cerc[:,0]][:,3], dist_cerc

    def get_route_relation_from_trackpoint(self, track_points):
        originNode, destinyNode, distance = self.get_closest_node(track_points)
        return np.column_stack((track_points, originNode, destinyNode, distance * 1000))

    def get_road_gaps(self,origin_point, target_point):
        route = nx.shortest_path(self.graph, origin_point, target_point)
        points = []
        for i in range(0, len(route) - 1):
            points.append((route[i], route[i + 1]))
        return np.array(points)

    def __closest_node(self,node, nodes):
        deltas = nodes - node
        dist_2 = np.einsum('ij,ij->i', deltas, deltas)
        return np.argmin(dist_2)

    def __haversine_distance(self, origin_point, target_point):
        """ Haversine formula to calculate the distance between two lat/long points on a sphere """
        radius = 6371.0  # FAA approved globe radius in km
        dlat = math.radians(target_point[0] - origin_point[0])
        dlon = math.radians(target_point[1] - origin_point[1])
        a = math.sin(dlat / 2.) * math.sin(dlat / 2.) + math.cos(math.radians(origin_point[0])) \
            * math.cos(math.radians(target_point[0])) * math.sin(dlon / 2.) * math.sin(dlon / 2.)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d * 1000

    def __get_points_distance(self, point, routeGap):
        #    nodes = data[(data[:, 2] == routeGap[0]) & (data[:, 3] == routeGap[1])][:, 0:2]
        nodes = self.df[(self.df['source'] == routeGap[0]) & (self.df['target'] == routeGap[1])]
        if nodes.size == 0:
            nodes = self.df[(self.df['source'] == routeGap[1]) & (self.df['target'] == routeGap[0])]
        try:
            coords = nodes.iloc[0].geometry.coords[:]
            coordList = [list(reversed(item)) for item in coords]
            return self.__haversine_distance(point, coordList[self.__closest_node(point, np.array(coordList))])
        except:
            return 0

    def get_simplified_route_relation(self,route_relation):
        exp = []
        exp.append(route_relation[0])
        for idx in range(1,len(route_relation)):
            distance = nx.shortest_path_length(self.graph,route_relation[idx][2],route_relation[idx-1][3])
            point = [route_relation[idx][0],route_relation[idx][1]]
            if distance == 0:
                exp.append(route_relation[idx])
            elif 6 >= distance >= 1:
                routeGaps = (self.get_road_gaps(route_relation[idx][2],route_relation[idx-1][3])).tolist()
                addedPoints = [[route_relation[idx][0],route_relation[idx][1]] + x + [self.__get_points_distance(point,x)] for x in routeGaps]
                exp.append(route_relation[idx])
                exp.extend(addedPoints)
            else:
                print("distancia:" + str(distance))
        self.trackpoint_route_distance = np.array(exp)[:,4]
        return np.array(exp)

    def get_node_points(self, t):
        ruta_simplificada = []
        for b in t:
            lon = self.graph.node[b]['x']
            lat = self.graph.node[b]['y']
            ruta_simplificada.append([lat, lon])
        return np.array(ruta_simplificada)

    def plot_route(self, track):
        routes = []
        for i in track:
            routes.append(nx.shortest_path(self.graph, i[2], i[3], weight='length'))
        ox.plot_graph_routes(self.graph, routes, route_linewidth=1, orig_dest_node_size=3)

    def get_distance_point_to_point(self,set):
        DistanceBetweenPonints = []
        for idx in range(0, len(set) - 1):
            distan = self.__haversine_distance(set[idx],
                                        set[idx + 1])
            DistanceBetweenPonints.append(distan)
        DistanceBetweenPonints = [x for x in DistanceBetweenPonints if x != 0]
        self.trackpoint_distance = DistanceBetweenPonints

    def get_bearing_point_to_point(self,set):
        angulos = []
        for idx in range(0, len(set) - 1):
            point = tuple(set[idx])
            nextPoint = tuple(set[idx + 1])
            deg = self.__calculate_initial_compass_bearing(point, nextPoint)
            angulos.append(deg)

        angSinCero = [x for x in angulos if x != 0]
        self.trackpoint_bearing = angSinCero

    def __calculate_initial_compass_bearing(self,pointA, pointB):
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

    def getFrequencyRoute(data):
        cabecera = np.array(['X', 'Y', 'Origen', 'Destino', 'Exactitud'])
        dftemps = pd.DataFrame({'Origen': data[:, 2], 'Destino': data[:, 3]})
        frequency = dftemps.groupby(["Origen", "Destino"]).size()
        pFrequency = frequency / frequency.sum()
        return np.array([[b, c] for b, c in pFrequency.items()])