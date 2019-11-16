from entities.Analyzer import Analyzer
import networkx
from sklearn.neighbors import KDTree
from entities.TrackPoint_impl import TrackPoint as Point
from entities.Graph_impl import Graph
import numpy as np


class TrackAnalyzer(Analyzer):
    def __init__(self, graph: Graph, tracks):
        self.graph = graph
        self.tracks = tracks
        self.segmentDf = networkx.to_pandas_edgelist(graph)
        self.tree = self.set_kdtree()

    def analyze(self):
        pass

    def get_closest_segment_point(self, track_analysis, coord_list, origin_node, target_node, point):
        """
        Gets the closest point's index given a segment and a point.

        :param track_analysis: Object of TrackAnalyzer class
        :param coord_list: List of GPS points of the segment
        :param origin_node: Origin node of the segment
        :param target_node: Target node of the segment
        :param point: GPS point to identify
        :return: Index of the list of closest point of the coordinates' list
        """
        # Buscamos los puntos candidatos más cercanos.
        a, b = track_analysis.get_closest_nodes([[point[0], point[1]]], 15)
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

    def set_kdtree(self):
        segment_data = self.create_tree_structure()
        return KDTree(np.array([[a.latitude, a.longitude] for a, b in segment_data]), metric='euclidean')
