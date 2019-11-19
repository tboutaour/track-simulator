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


def haversine_distance(origin_point, target_point):
    """ Haversine formula to calculate the distance between two lat/long points on a sphere """
    radius = 6371.0  # FAA approved globe radius in km
    dlat = math.radians(target_point[0] - origin_point[0])
    dlon = math.radians(target_point[1] - origin_point[1])
    a = math.sin(dlat / 2.) * math.sin(dlat / 2.) + math.cos(math.radians(origin_point[0])) \
        * math.cos(math.radians(target_point[0])) * math.sin(dlon / 2.) * math.sin(dlon / 2.)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d * 1000


class HMM(HiddenMarkovModel):
    def __init__(self, graph):
        self.graph = graph
        # self.segmentDf = networkx.to_pandas_edgelist(graph.graph)
        # self.track_data = self.create_tree_structure()
        # self.tree = self.set_kdtree()

    def get_emission_prob(self, projection, point):
        d = (1 / (math.sqrt(2 * math.pi)) * SIGMA) * math.e ** (
                -(haversine_distance(projection[0], point[0])) ** 2 / (2 * SIGMA) ** 2)
        return d

    def get_transition_prob(self, graph, projection, prev_point):
        # dest = prev_point[1][0]
        shortest_path = math.e ** graph.get_shortest_path(prev_point[1][0], float(projection[1][0]))
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
            projections, _ = self.get_closest_nodes([points[idx_point]], 0.001)
            # Para cada una de las proyecciones obtner sus probabilidades
            # Nos quedaremos con la proyección de mayor probabilidad
            for projection in projections:
                emission_prob = self.get_emission_prob([points[idx_point]], projection)
                if idx_point > 1:
                    total_prob = emission_prob * self.get_transition_prob(projection, path[-1])
                else:
                    total_prob = emission_prob * 1.0
                if total_prob > max_prob:
                    estimated_point = projection
                    max_prob = total_prob
            if idx_point > 0:
                # Si la distancia entre puntos es mayor a 1 se debe completar el camino.
                distance_between_points = networkx.shortest_path_length(self.graph, path[-1][1][1],
                                                                        estimated_point[1][0])
                if 8 > distance_between_points >= 1 and (path[-1][1] != estimated_point[1]):
                    self.complete_path(path, estimated_point)
                elif distance_between_points <= 0 or (path[-1][1] == estimated_point[1]):
                    path.append(estimated_point)
            else:
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

    def set_kdtree(self):
        return KDTree(np.array([[a.latitude, a.longitude] for a, b in self.track_data]), metric='euclidean')

    def get_closest_nodes(self, points: Point):
        nearest_edges = self.get_nearest_edge(points)
        [print(i[0][0]) for i in nearest_edges]
        return [TrackSegment(edge[0][0].coords[:]).get_nearest_point_from_segment(Point(tuple(reversed(points.get_latlong())))) for edge in nearest_edges]

    def create_tree_structure(self):
        """
        Creation of the structure to set the KDtree.
        For every geometry, extract every point and create array.
        :return: Array composed by [Coord Point,Source,Target]
        """
        road_relation = self.segmentDf[['source', 'target', 'geometry']]
        n = []
        for road in road_relation.iterrows():
            try:
                coords = road[1].geometry.coords[:]
                coord_list = [(Point(y, x)) for x, y in coords]
                L = [[coord_point, (road[1].source, road[1].target)] for coord_point in coord_list]
                n.extend(L)
            except AttributeError:
                pass
        return np.array(n)

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
        closest_edges_to_point = edges_with_distances[:2]

        return closest_edges_to_point
