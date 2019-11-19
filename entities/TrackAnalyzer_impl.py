from entities.Analyzer import Analyzer
import networkx
from sklearn.neighbors import KDTree

from entities.TrackAnalyzerStatistics_impl import TrackAnalyzerStatistics
from entities.TrackPoint_impl import TrackPoint as Point
from entities.Graph_impl import Graph
import numpy as np
import logging
from entities.TrackSegment_impl import TrackSegment


class TrackAnalyzer(Analyzer):
    def __init__(self, graph: Graph, tracks, statistics: [TrackAnalyzerStatistics]):  # Estas tracks deben estar ya detectadas y filtradas
        self.graph = graph
        self.tracks = tracks
        self.statistics = statistics



    # TODO implement Analyze functionality
    def analyze(self):
        """
        Analyze the track.
        Obtain trackpoint distance and the mapping of the track.
        :param track:
        :return:
        """
        self.__get_trackpoint_distance(self.tracks)
        analyzed_track, m = self.__viterbi_algorithm(self.tracks)
        simplified_track = self.__get_simplified_route_relation(analyzed_track)
        return analyzed_track, m, simplified_track

    def get_closest_segment_point(self, coord_list, origin_node, target_node, point):
        """
        Gets the closest point's index given a segment and a point.

        :param coord_list: List of GPS points of the segment
        :param origin_node: Origin node of the segment
        :param target_node: Target node of the segment
        :param point: GPS point to identify
        :return: Index of the list of closest point of the coordinates' list
        """
        # Buscamos los puntos candidatos más cercanos.
        a, b = self.get_closest_nodes([[point[0], point[1]]], 15)
        aux = []
        # Filtramos aquellos que pertenecen a la ruta en cuestión
        for idx in range(0, len(a)):
            aux.append([a[idx][0], a[idx][1], b[0][idx]])

        # Ordenamos por distancia
        aux = sorted(aux, key=lambda x: x[2])
        correct_aux = [a for a in aux if a[1] == (origin_node, target_node)]

        # Sacamos el índice del punto más cercano (primero de la lista) dentro de la lista de puntos del segmento
        try:
            idx = coord_list.index([correct_aux[0][0][0], correct_aux[0][0][1]])
        except (ValueError, IndexError):
            # Si falla devolvemos directamente el final
            idx = len(coord_list)
        return idx






    def get_mid_track_point(self, origin, target):
        nodes = self.segmentDf[(self.segmentDf['source'] == origin) & (self.segmentDf['target'] == target)]
        if nodes.size == 0:
            nodes = self.segmentDf[(self.segmentDf['source'] == target) & (self.segmentDf['target'] == origin)]
        try:
            segment = TrackSegment(nodes.iloc[0].geometry.coords[:])
            return segment.get_middle_point()
        except Exception as e:
            logging.error("Cannot get middle_point:", exc_info=True)
