from entities.HiddenMarkovModel import HiddenMarkovModel
import math
import networkx
import numpy as np
from entities.TrackPoint import TrackPoint as Point
import osmnx
import logging
from entities.TrackSegment import TrackSegment

SIGMA = 4
BETA = 0.1


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

    def get_emission_prob(self, point, projection):
        # d = (1 / (math.sqrt(2 * math.pi)) * SIGMA) * math.e ** (
        #         -(haversine_distance(point, projection[0])) ** 2 / (2 * SIGMA) ** 2)

        c = (1 / (SIGMA * math.sqrt(2 * math.pi)))
        distancia = osmnx.great_circle_vec(point.get_latitude(),
                                           point.get_longitude(),
                                           projection[0].get_latitude(),
                                           projection[0].get_longitude())
        prob = c * math.e ** (-0.5 * ((distancia / SIGMA) ** 2))
        return prob
        # return d

    def get_transition_prob(self, point, projection, next_point, next_projection):
        great_circle_distance = osmnx.great_circle_vec(point.get_latitude(),
                                          point.get_longitude(),
                                          next_point.get_latitude(),
                                          next_point.get_longitude())
        route_distance = self.graph.get_shortest_path_length(projection[2],
                                                            next_projection[1])

        prob = (1 / BETA) * math.e ** (-(abs(great_circle_distance - route_distance)))
        return prob

    def viterbi_algorithm(self, points):
        path = []
        max_prob_record = []
        # Para cada uno de los puntos GPS
        for idx_point in range(0, len(points) - 1):
            max_prob = 0
            total_prob = 0
            # Obtención de todas las proyecciones de este punto
            projections = self.get_closest_nodes(points[idx_point])
            future_projections = self.get_closest_nodes(points[idx_point + 1])
            # Para cada una de las proyecciones obtner sus probabilidades
            # Nos quedaremos con la proyección de mayor probabilidad
            for projection in projections:
                emission_prob = self.get_emission_prob(points[idx_point], projection)
                if idx_point > 0:
                    # total_prob = max(map(emission_prob * self.get_transition_prob(projection, path[-1])))
                    temporal = [
                        emission_prob * self.get_transition_prob(points[idx_point], projection, points[idx_point + 1],
                                                                 f_proj) for f_proj in future_projections]
                    total_prob = max(temporal)
                else:
                    total_prob = emission_prob * 1.0
                if total_prob > max_prob:
                    if idx_point > 1:
                        if (projection[2] == path[-1][1]) or (projection[2] == path[-1][2] and projection[1] != path[-1][1]):
                            projection[1], projection[2] = projection[2], projection[1]
                    estimated_point = projection
                    max_prob = total_prob
                    if idx_point > 0 and self.graph.get_shortest_path_length(projection[1], path[-1][1]) > 2:
                        logging.debug("Se añade un camino con distancia > 2")
            path.append(estimated_point)
            max_prob_record.append(max_prob)
        return path, max_prob_record

    def get_closest_nodes(self, points: Point):
        nearest_edges = self.get_nearest_edge(points)
        return [[TrackSegment(edge[0][0].coords[:]).get_nearest_point_from_segment(points), edge[0][1], edge[0][2]] for
                edge in nearest_edges]

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
        closest_edges_to_point = edges_with_distances[:4]

        return closest_edges_to_point
