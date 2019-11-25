from entities.HiddenMarkovModel import HiddenMarkovModel
import math
import networkx
import numpy as np
from sklearn.neighbors import KDTree
from entities.TrackAnalyzer_impl import TrackAnalyzer
from entities.TrackPoint_impl import TrackPoint as Point
from entities.Graph_impl import Graph
import osmnx

from entities.TrackSegment_impl import TrackSegment

SIGMA = 1.6


def haversine_distance(origin_point: Point, target_point: Point):
    """ Haversine formula to calculate the distance between two lat/long points on a sphere """
    radius = 6371.0  # FAA approved globe radius in km
    dlat = math.radians(target_point.get_latitude() - origin_point.get_latitude())
    dlon = math.radians(target_point.get_longitude() - origin_point.get_longitude())
    a = math.sin(dlat / 2.) * math.sin(dlat / 2.) + math.cos(math.radians(origin_point.get_latitude())) \
        * math.cos(math.radians(target_point.get_latitude())) * math.sin(dlon / 2.) * math.sin(dlon / 2.)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d * 1000


class HMM(HiddenMarkovModel):
    def __init__(self, graph):
        self.graph = graph
        # self.segmentDf = networkx.to_pandas_edgelist(graph.graph)
        # self.track_data = self.create_tree_structure()
        # self.tree = self.set_kdtree()

    def get_emission_prob(self, point, projection):
        # d = (1 / (math.sqrt(2 * math.pi)) * SIGMA) * math.e ** (
        #         -(haversine_distance(point, projection[0])) ** 2 / (2 * SIGMA) ** 2)

        c = 1 / (SIGMA * math.sqrt(2 * math.pi))
        return c * math.exp(-osmnx.great_circle_vec(point.get_latitude(),
                                                    point.get_longitude(),
                                                    projection[0].get_latitude(),
                                                    projection[0].get_longitude()) ** 2)
        # return d

    def get_transition_prob(self, projection, prev_point):
        # dest = prev_point[1][0]
        shortest_path = math.e ** self.graph.get_shortest_path(prev_point[0],
                                                               projection[0])
        # shortest_path = nx.shortest_path_length(self.graph,prev_point[1][0],float(projection[1][0]))+1
        distance = haversine_distance(prev_point[0], projection[0])
        prob = distance / shortest_path
        return prob

    def viterbi_algorithm(self, points):
        path = []
        max_prob_record = []
        # Para cada uno de los puntos GPS
        for idx_point in range(0, len(points)):
            max_prob = 0
            total_prob = 0
            # Obtención de todas las proyecciones de este punto
            projections = self.get_closest_nodes(points[idx_point])
            # Para cada una de las proyecciones obtner sus probabilidades
            # Nos quedaremos con la proyección de mayor probabilidad
            for projection in projections:
                emission_prob = self.get_emission_prob(points[idx_point], projection)
                if idx_point > 0:
                    total_prob = emission_prob * self.get_transition_prob(projection, path[-1])
                else:
                    total_prob = emission_prob * 1.0
                if total_prob > max_prob:
                    estimated_point = projection
                    max_prob = total_prob
            path.append(estimated_point)
            max_prob_record.append(max_prob)
        return path, max_prob_record

    def complete_path(self, path, point):
        aux_path = networkx.shortest_path(self.graph, path[-1][1][1], point[1][0])
        points = []
        for i in range(0, len(aux_path) - 1):
            mid_point = self.get_mid_track_point(aux_path[i], aux_path[i + 1])
            # print(aux_path[i], aux_path[i + 1],mid_point)
            if mid_point is not None:
                path.append(np.array([path[-1][0], (aux_path[i], aux_path[i + 1])]))
            else:
                path.append(np.array([point[0], (aux_path[i], aux_path[i + 1])]))
        path.append(point)

    def get_closest_nodes(self, points: Point):
        nearest_edges = self.get_nearest_edge(points)
        for n in nearest_edges:
            print(n)

        return [[TrackSegment(edge[0][0].coords[:]).get_nearest_point_from_segment(points), edge[0][1], edge[0][2]] for edge in nearest_edges]

    def get_nearest_edge(self, point):
        gdf = osmnx.graph_to_gdfs(self.graph.graph, nodes=False, fill_edge_geometry=True)
        graph_edges = gdf[["geometry", "u", "v"]].values.tolist()

        edges_with_distances = [
            (
                graph_edge,
                Point(tuple(reversed(point.get_latlong()))).distance(graph_edge[0])
            )
            for graph_edge in graph_edges
        ]

        edges_with_distances = sorted(edges_with_distances, key=lambda x: x[1])
        closest_edges_to_point = edges_with_distances[:3]
        return closest_edges_to_point
