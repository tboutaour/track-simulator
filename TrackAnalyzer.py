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
from geopy import Point as gPoint
from itertools import groupby
from shapely.geometry import Point, LineString

DEL_ATTRIB = ['tunnel','access','oneway','name','osmid','service','lanes','bridge','ref','maxspeed','highway']
SIGMA = 1.6

class TrackAnalyzer:
    def __init__(self, north, south, east, west):
        self.graph = self.initialize_graph(north, south, east, west)
        self.df = nx.to_pandas_edgelist(self.graph)
        self.trackpoint_distance = []
        self.trackpoint_route_distance = []
        self.trackpoint_bearing = []
        self.trackpoint_number = []
        self.route_data = []
        self.__tree = -1
        self.__set_kdtree()

    #Pasado modificado a clase Graph
    def initialize_graph(self, north, south, east, west):
        aux_graph = ox.graph_from_bbox(north, south, east, west)
        graph = self.completar_grafo(aux_graph)
        graph = aux_graph
        edges = list(graph.edges)
        zeros = [0] * len(edges)
        ones = [1] * len(edges)
        dic_reg_zeros = dict(zip(edges, zeros))
        dic_reg_ones = dict(zip(edges, ones))
        nx.set_edge_attributes(graph, dic_reg_ones, 'num of detections')
        nx.set_edge_attributes(graph, dic_reg_zeros, 'num of points')
        self.__initialize_path_freq(graph, edges)
        return graph

    #Pasado a clase graph
    def __initialize_path_freq(self, graph, edges):
        list_prob = []
        for edge in edges:
            number = len(graph.edges(edge[0]))
            prob = 1 / number
            list_prob.append(prob)
        dic_freq = dict(zip(edges, list_prob))
        nx.set_edge_attributes(graph, dic_freq, 'frequency')

    #Pasado a Clase Graph
    def __update_edge_freq(self, source_node, target_node):
        """
        Update information of edge frequency in detection. This method updates information in all edges given the source.
        This update the TrackAnalyzer object.
        :param source_node: Source node of the edge visited
        :param target_node: Target node of the edge visited
        """
        self.graph.edges[(source_node, target_node, 0)]['num of detections'] +=1
        total = self.df['num of detections'][self.df['source'] == source_node].sum()
        for edge in self.graph.edges(source_node):
            self.graph.edges[(edge[0],edge[1],0)]['frequency'] = self.graph.edges[(edge[0],edge[1],0)]['num of detections']/total
        self.df = nx.to_pandas_edgelist(self.graph, source='source', target='target')


    def __update_frequencies(self,track_points):
        for track_point in track_points:
            self.__update_edge_freq(track_point[0],track_point[1])


    def __get_trackpoint_distance(self, track_points):
        for p in range(0,len(track_points) - 1):
            self.trackpoint_distance.append(distance(track_points[p], track_points[p + 1]).km)

    def create_tree_structure(self):
        """
        Creation of the structure to set the KDtree.
        For every geometry, extract every point and create array.
        :return: Array composed by [Coord Point,Source,Target]
        """
        road_relation = self.df[['source', 'target', 'geometry']]
        n = []
        for road in road_relation.iterrows():
            try:
                coords = road[1].geometry.coords[:]
                coord_list = [(gPoint(y,x)) for x,y in coords]
                L = [[coord_point ,(road[1].source, road[1].target)] for coord_point in coord_list]
                n.extend(L)
            except AttributeError:
                pass
        return np.array(n)

    def __set_kdtree(self):
        self.route_data = self.create_tree_structure()
        self.__tree = KDTree(np.array([[a.latitude,a.longitude] for a,b in self.route_data]), metric='euclidean')

    def get_closest_nodes(self, puntos,radius):
        idx_cerc,dist = self.__tree.query_radius(puntos, r=radius, count_only=False, return_distance=True)
        return np.array(self.route_data[idx_cerc[0]]), dist

    # pasado a clase HMM
    def __get_emission_prob(self,projection, point):
        d = (1/(math.sqrt(2*math.pi))*SIGMA)*math.e**(-(self.__haversine_distance(projection[0],point[0]))**2/(2*SIGMA)**2)
        return d

    # pasado a clase HMM
    def __get_transition_prob(self,projection,prev_point):
        dest = prev_point[1][0]
        try:
            shortest_path = math.e**((nx.shortest_path_length(self.graph,prev_point[1][0],float(projection[1][0]))))
            #shortest_path = nx.shortest_path_length(self.graph,prev_point[1][0],float(projection[1][0]))+1
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

    # pasado a clase HMM
    def complete_path(self, path, point):
        aux_path = nx.shortest_path(self.graph, path[-1][1][1], point[1][0])
        points = []
        for i in range(0, len(aux_path) - 1):
            mid_point = self.get_mid_track_point(aux_path[i], aux_path[i + 1])
            # print(aux_path[i], aux_path[i + 1],mid_point)
            if mid_point is not None:
                path.append(np.array([path[-1][0],(aux_path[i], aux_path[i + 1])]))
            else:
                path.append(np.array([point[0], (aux_path[i], aux_path[i + 1])]))
        path.append(point)

    # pasado a clase HMM
    def __viterbi_algorithm(self,points):
        path = []
        max_prob_record = []
        # Para cada uno de los puntos GPS
        for idx_point in range(0,len(points)):
            max_prob = 0
            total_prob = 0
            #Obtención de todas las proyecciones de este punto
            projections,_ = self.get_closest_nodes([points[idx_point]], 0.001)
            #Para cada una de las proyecciones obtner sus probabilidades
            #Nos quedaremos con la proyección de mayor probabilidad
            for projection in projections:
                emission_prob = self.__get_emission_prob([points[idx_point]], projection)
                if idx_point > 1:
                    total_prob = emission_prob * self.__get_transition_prob(projection, path[-1])
                else:
                    total_prob = emission_prob * 1.0
                if total_prob > max_prob:
                    estimated_point = projection
                    max_prob = total_prob
            if idx_point > 0:
                #Si la distancia entre puntos es mayor a 1 se debe completar el camino.
                distance_between_points = nx.shortest_path_length(self.graph, path[-1][1][1],estimated_point[1][0])
                if 8 > distance_between_points >= 1 and (path[-1][1] != estimated_point[1]):
                    self.complete_path(path,estimated_point)
                elif distance_between_points <= 0 or (path[-1][1] == estimated_point[1]):
                    path.append(estimated_point)
            else:
                path.append(estimated_point)
            max_prob_record.append(max_prob)
        return path, max_prob_record

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

    # pasado a clase HMM
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
        nodes = self.df[(self.df['source'] == routeGap[0]) & (self.df['target'] == routeGap[1])]
        if nodes.size == 0:
            nodes = self.df[(self.df['source'] == routeGap[1]) & (self.df['target'] == routeGap[0])]
        try:
            coords = nodes.iloc[0].geometry.coords[:]
            coordList = [list(reversed(item)) for item in coords]
            return self.__haversine_distance(point, coordList[self.__closest_node(point, np.array(coordList))])
        except:
            return 0

    def __get_simplified_route_relation(self, route_relation):
        """
        Currently deprecated.
        Add points between routes.
        :param route_relation: route to analyze gaps.
        :return: route without gaps
        """
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
                # print("distancia:" + str(distance))
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

    def __get_distance_point_to_point(self, set):
        DistanceBetweenPonints = []
        for idx in range(0, len(set) - 1):
            distan = self.__haversine_distance(set[idx],
                                               set[idx + 1])
            DistanceBetweenPonints.append(distan)
        DistanceBetweenPonints = [x for x in DistanceBetweenPonints if x != 0]
        self.trackpoint_route_distance = DistanceBetweenPonints

    def __get_bearing_point_to_point(self, set):
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

    def get_idx(self, par):
        return self.df.loc[(self.df['source'] == par[0]) & (self.df['target'] == par[1])].index[0]

    def __get_number_points(self,set):
        """
        Obtain number of points of a set and save the information.
        This update the TrackAnalyzer object.
        :param set: Set of GPS points
        """
        count = [len(list(group)) for key, group in groupby(sorted(set))]
        self.trackpoint_number.extend(count)


    def analyze_results(self,track):
        """
        Obtain the information from the track
        This information are the following:
        -Trackpoint distance: Distance between x point and the nearest point of the real track
        -Bearing: Bearing between x and x+1 points of the track
        -Number of points: Number of points by segment of the track
        -Distance point to point: Distance between x and x+1 points of the track
        -Frequencies: Frequencies of aparition of the segment of a route
        :param track: List of GPS points (lat,lon) referenced by the nearest segment
        """
        #self.__get_trackpoint_distance(track[:,0])
        self.__get_bearing_point_to_point(track[:,0])
        self.__get_number_points(track[:, 1])
        self.__get_distance_point_to_point(track[:,0])
        self.__update_frequencies(track[:,1])


    def completar_grafo(self,graph):
        """
        From the graph realize a copy and convertes it in a directed graph with de geometrical information of route
        inveted.
        :param graph: Graph to realitze a directed copy.
        :return: Directed copy of the graph passed by parameter.
        """
        graph_aux = graph.copy()
        for edge in graph_aux.edges(data=True):
            try:
                #crearemos la arista
                reverted = edge
                attr = reverted[2]
                #Almacenamos la información de los puntos
                a = reverted[2]['geometry'].coords[:]
                #Giramos los puntos (están en a)
                a.reverse()
                reverted[2]['geometry'] = LineString(a)
                e = (reverted[1],reverted[0],0)
                # print("Vamos a añadir: ",e,attr)
                graph.add_edge(*e,**attr)
            except KeyError:
                attr = reverted[2]
                e = (reverted[1], reverted[0],0)
                graph.add_edge(*e, **attr)
                # graph.edges[(edge[0], edge[1], 0)]['oneway'] = False
        # for n1, n2, d in graph.edges(data=True):
        #     for att in DEL_ATTRIB:
        #         d.pop(att, None)
        return graph

    def analize_track(self,track):
        """
        Analyze the track.
        Obtain trackpoint distance and the mapping of the track.
        :param track:
        :return:
        """
        self.__get_trackpoint_distance(track)
        analyzed_track, m = self.__viterbi_algorithm(track)
        simplified_track = self.__get_simplified_route_relation(analyzed_track)
        return analyzed_track, m, simplified_track

    def compose_file_information(self,graph):
        """
        Compose information between self graph and the imported graph.
        :param graph: imported graph with different information
        """
        self.graph = nx.compose(self.graph,graph)
        self.df = nx.to_pandas_edgelist(self.graph)