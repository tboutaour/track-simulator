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
from geopy import Point


class TrackAnalyzer:
    def __init__(self, north, south, east, west):
        self.graph = self.initialize_graph(north, south, east, west)
        self.df = nx.to_pandas_edgelist(self.graph,source = 'source',target='target')
        self.trackpoint_distance = []
        self.trackpoint_route_distance = []
        self.trackpoint_bearing = []
        self.route_data = []
        self.__tree = -1

    def initialize_graph(self, north, south, east, west):
        graph = ox.graph_from_bbox(north, south, east, west).to_undirected().to_directed()
        edges = list(graph.edges)
        zeros = [0] * len(edges)
        ones = [1] * len(edges)
        dic_reg_zeros = dict(zip(edges, zeros))
        dic_reg_ones = dict(zip(edges, ones))
        # nx.set_edge_attributes(graph, dic_reg_zeros, 'num of regs')
        nx.set_edge_attributes(graph, dic_reg_ones, 'num of detections')
        nx.set_edge_attributes(graph, dic_reg_zeros, 'num of points')
        self.initialize_path_freq(graph, edges)
        return graph

    def initialize_path_freq(self, graph, edges):
        list_prob = []
        for edge in edges:
            number = len(graph.edges(edge[0]))
            prob = 1 / number
            list_prob.append(prob)
        dic_freq = dict(zip(edges, list_prob))
        nx.set_edge_attributes(graph, dic_freq, 'frequency')

    def update_graph_information(self, dataset):
        old_information = self.df['source', 'target',]
        dict_ = {(x[0], x[0], 0): y for x, y in dataset.groupby(['source', 'target']).size().items()}

    def update_edge_freq(self, source_node, target_node):
        self.graph.edges[(source_node, target_node, 0)]['num of detections'] +=1
        total = self.df['num of detections'][self.df['source'] == source_node].sum()
        for edge in self.graph.edges(source_node):
            self.graph.edges[(edge[0],edge[1],0)]['frequency'] = self.graph.edges[(edge[0],edge[1],0)]['num of detections']/total
        self.df = nx.to_pandas_edgelist(self.graph, source='source', target='target')

    def get_trackpoint_distance(self, track_points):
        for p in range(0,len(track_points) - 1):
            self.trackpoint_distance.append(distance(track_points[p], track_points[p + 1]).m)

    # Función para generar el array bidimensional con todos los puntos DE LA RUTA y sus nodos or. fin.
    def create_tree_structure(self):
        roadRelation = self.df[['source', 'target', 'geometry']]
        n = []
        for road in roadRelation.iterrows():
            try:
                coords = road[1].geometry.coords[:]
                coordList = [(Point(y,x)) for x,y in coords]
                L = [[c ,(road[1].source, road[1].target)] for c in coordList]
                n.extend(L)
            except AttributeError:
                pass
        return np.array(n)

    def set_kdtree(self):
        self.route_data = self.create_tree_structure()
        self.__tree = KDTree(np.array([[a.latitude,a.longitude] for a,b in self.route_data]), metric='euclidean')

    def get_closest_nodes(self, puntos,radius):
        idx_cerc,dist = self.__tree.query_radius(puntos, r=radius, count_only=False, return_distance=True)
        return np.array(self.route_data[idx_cerc[0]]), dist

    def get_emission_prob(self,projection, point):
        d = (1/(math.sqrt(2*math.pi)))*math.e**(-(self.__haversine_distance(projection[0],point[0]))/2)
        return d

    def get_transition_prob(self,projection,prev_point):
        # print(projection[1][0])
        # print(point[1][0])
        # print(projection[0])
        # print(point[0])
        dest = prev_point[1][0]
        try:
            shortest_path = math.e**((nx.shortest_path_length(self.graph,prev_point[1][0],float(projection[1][0])))*7)
        except nx.NetworkXNoPath:
            shortest_path = math.e**100
        distance = self.__haversine_distance(prev_point[0],projection[0])
        prob = distance/shortest_path
        return prob

    def get_mid_track_point(self, origin, target):
        nodes = self.df[(self.df['source'] == origin) & (self.df['target'] == target)]
        if nodes.size == 0:
            nodes = self.df[(self.df['source'] == target) & (self.df['target'] == origin)]
        try:
            coords = nodes.iloc[0].geometry.coords[:]
            mid_point = Point((coords[int((len(coords) / 2))][1],coords[int((len(coords) / 2))][0]))
            return mid_point
        except:
            pass

    def complete_path(self, path, point):
        aux_path = nx.shortest_path(self.graph, path[-1][1][1], point[1][0])
        points = []
        for i in range(0, len(aux_path) - 1):
            mid_point = self.get_mid_track_point(aux_path[i], aux_path[i + 1])
            print(aux_path[i], aux_path[i + 1],mid_point)
            if mid_point is not None:
                path.append(np.array([mid_point,(aux_path[i], aux_path[i + 1])]))
            else:
                path.append(np.array([point[0], (aux_path[i], aux_path[i + 1])]))
        path.append(point)

    def viterbi_algorithm(self,points):
        path = []
        max_scores = []
        # Para cada uno de los puntos GPS
        for idx_point in range(0, len(points)):
            print("idx "+str(idx_point))
            max_score = 0
            score = 0
            projections,_ = self.get_closest_nodes([points[idx_point]], 0.001)
            print("cant.punt "+str(len(projections)))
            for p in projections:
                ep = self.get_emission_prob([points[idx_point]], p)
                if idx_point > 1:
                    score = ep * self.get_transition_prob(p, path[-1])
                else:
                    score = ep * 1.0
                if score > max_score:
                    estimated = p
                    max_score = score
                # print(path[-1][1][1])
                # print(estimated[1][0])
            if idx_point > 0:
                distance = nx.shortest_path_length(self.graph, path[-1][1][1],estimated[1][0])
                print("distance "+str(distance))
                if 8 > distance >= 1:
                    print("Completamos Path")
                    self.complete_path(path,estimated)
                elif distance <= 0:
                    path.append(estimated)
            else:
                path.append(estimated)
            max_scores.append(max_score)
        return path, max_scores

    def get_road_gaps(self, origin_point, target_point):
        route = nx.shortest_path(self.graph, origin_point, target_point)
        points = []
        for i in range(0, len(route) - 1):
            points.append((route[i], route[i + 1]))
        return np.array(points)

    def __closest_node(self, node, nodes):
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

    def get_simplified_route_relation(self, route_relation):
        exp = []
        exp.append(route_relation[0])
        for idx in range(1, len(route_relation)):
            distance = nx.shortest_path_length(self.graph, route_relation[idx][1][1], route_relation[idx - 1][1][0])
            point = [route_relation[idx][0], route_relation[idx][1]]
            if distance == 0:
                exp.append(route_relation[idx])
            elif 2 >= distance > 0:
                routeGaps = (self.get_road_gaps(route_relation[idx][1][1], route_relation[idx - 1][1][0])).tolist()
                addedPoints = [
                     [route_relation[idx][0], tuple(x)] for x
                     in routeGaps]
                exp.append(route_relation[idx])
                exp.extend(addedPoints)
            else:
                print("distancia:" + str(distance))
                idx += 2
        # self.trackpoint_route_distance = np.array(exp)[:, 4]
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

    def get_distance_point_to_point(self, set):
        DistanceBetweenPonints = []
        for idx in range(0, len(set) - 1):
            distan = self.__haversine_distance(set[idx],
                                               set[idx + 1])
            DistanceBetweenPonints.append(distan)
        DistanceBetweenPonints = [x for x in DistanceBetweenPonints if x != 0]
        self.trackpoint_distance = DistanceBetweenPonints

    def get_bearing_point_to_point(self, set):
        angulos = []
        for idx in range(0, len(set) - 1):
            point = tuple(set[idx])
            nextPoint = tuple(set[idx + 1])
            deg = self.__calculate_initial_compass_bearing(point, nextPoint)
            angulos.append(deg)

        angSinCero = [x for x in angulos if x != 0]
        self.trackpoint_bearing = angSinCero

    def __calculate_initial_compass_bearing(self, pointA, pointB):
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

    def getFrequencyRoute(self, data):
        # cabecera = np.array(['X', 'Y', 'Origen', 'Destino', 'Exactitud'])
        dftemps = pd.DataFrame({'Origen': data[:, 2], 'Destino': data[:, 3]})
        frequency = dftemps.groupby(["Origen", "Destino"]).size()
        pFrequency = frequency / frequency.sum()
        return np.array([[b, c] for b, c in pFrequency.items()])

    def setFrequencyToNode(self, data):
        # En item[0] tendremos (origen,destino)
        # En item[1] tendremos porcentaje frecuencia

        # la idea es ir al nodo, coger el atributo que corresponde con
        # el destino y añadirle la frecuencia
        for item in data:
            try:
                self.graph.nodes[item[0][0]]["prob"].append([item[0][1], item[1]])
            except KeyError:
                self.graph.nodes[item[0][0]]["prob"] = [[item[0][1], item[1]]]

    def get_idx(self, par):
        return self.df.loc[(self.df['source'] == par[0]) & (self.df['target'] == par[1])].index[0]

    def create_route(self, results):
        L = [(x[0], x[1], 0) for x in results[:, 1]]
        idss = [n for i, n in enumerate(L) if i == 0 or n != L[i - 1]]
        ids = []
        for i in idss:
            ids.append(i[0])
        return ids