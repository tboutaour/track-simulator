import abc

class Analizer(abc.ABC):
    @abc.abstractmethod
    def analyze(self):
        """."""
        return

    def generateResults(self):
        """."""
        return

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

