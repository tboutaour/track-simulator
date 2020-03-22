from src.track_analyzer.interactor.simulator import Simulator
from src.track_analyzer.entities.graph import Graph
from src.track_analyzer.entities.statistics import Statistics
from src.track_analyzer.entities.track_point import TrackPoint

import numpy as np
import utils
import geopy
import geopy.distance
import math

NUMBER_SIMULATIONS = 4
PROB_RETURN = 0.4


class TrackSimulator(Simulator):
    def __init__(self, graph: Graph, statistics: Statistics):
        self.graph = graph
        self.statistics = statistics

    def simulate(self):
        pass

    def simulate_route(self, origin, end, distance, ax):
        """
        Simulates creation of route given an origin and target point.
        This simulation is made by searching Dijkstra's path and simulating points segment by segment.

        :param track_analysis: Object of track_analyzer class
        :param origin: Origin node of the simulated route
        :param end: Target node of the simulated route
        :param ax: axes for plotting points
        :return: Numpy array of points of the simulated route
        """
        simulated_track = []
        # Simular creación de trayectoria completa

        # Encontrar el camino más probable.
        list_original = []
        list_distances = []
        list_reduced = []

        # Realizamos 5 y nos quedamos con el que tenga menos repeticiones.
        for i in range(0, NUMBER_SIMULATIONS):
            simulated_path_aux, distance_generated = self.create_path(origin, distance)
            list_original.append(simulated_path_aux)
            list_distances.append(distance_generated)
            res = []
            res = [l for l in simulated_path_aux if l not in res]
            list_reduced.append(res)

        idx_to_return = list_reduced.index(max(list_reduced, key=len))
        simulated_path = list_original[idx_to_return]
        distance_to_return = list_distances[idx_to_return]

        # Iterar para cada uno de los nodos del camino escogido
        path = []
        for d in range(0, len(simulated_path) - 1):
            path.append([simulated_path[d], simulated_path[d + 1]])

        # Lista de colores para los segmentos
        colors = ["green", "red", "blue", "purple", "pink", "orange", "yellow", "black"]

        # Indice para crear segmentos de colores distintos
        idx_color = 0
        for segment in path:
            seg = self.simulate_segment(segment)
            idx_color = idx_color + 1
            for s in seg:
                simulated_track.append(s)

        return np.array(simulated_track), distance_to_return

    def create_path(self, origin, dist):
        """
        Create the most frequent path given frequencies stored at track_analysis object.
        Given an origin node and a maximum distance it creates the most frequent path.
        Once the track_analysis is updated the path may change.
        It does not recognise returns of route.
        :param origin: Origin node of the simulated route
        :param dist: Distance of the route.
        :return: created path, distance of this path.
        """
        path = []
        distance_created = 0
        prev_node = origin
        path.append(origin)
        while distance_created < dist:
            next_node = self.get_most_frequent_node(prev_node, path)
            distance_aux = distance_created + self.graph.get_edge_by_nodes(prev_node, next_node)['length']
            if distance_aux < dist:
                distance_created = distance_aux
                path.append(next_node)
                prev_node = next_node
            else:
                return path, distance_created
        return path, distance_created

    def simulate_segment(self, segment):
        aux = 0
        origin_node = segment[0]
        target_node = segment[1]
        segment = []
        origin_point = TrackPoint(self.graph.get_nodes()[origin_node]['x'], self.graph.get_nodes()[origin_node]['y'])
        target_point = TrackPoint(self.graph.get_nodes()[target_node]['x'], self.graph.get_nodes()[target_node]['y'])
        try:
            dest, aux = self.calculate_point(segment, origin_node, target_node, origin_point, target_point)
            next = dest
            while aux > 24 and len(segment) < 30:
                dest, aux = self.calculate_point(segment, origin_node, target_node, next, target_point)
                next = dest
        except KeyError:
            pass
        return segment

    def calculate_point(self, segment, origin_node, target_node, origin_point: TrackPoint, segment_target_point: TrackPoint):
        """
        Calculates the point for the simulated segment.
        This point is calculated by a distance and a bearing.
        While the distance from the generated point to the closest point of the segment is not sustainable we recalculate
        the point.

        :param segment: Segment related to the generated point
        :param origin_node: Origin node of the segment
        :param target_node: Target node of the segment
        :param origin_point: Origin GPS point
        :param segment_target_point: Target point of the segment
        :return:
        """
        # Cargar la estructura de lista del segmento
        coords = self.graph.get_edge_by_nodes(origin_node, target_node)['geometry'].coords[:]
        coord_list = [tuple(item) for item in coords]

        # Calcular el punto GPS más cercano del segmento
        idx = self.get_closest_segment_point(coord_list, origin_point)

        # Calculamos la dirección entre el punto que origen y el siguiente punto encontrado
        try:
            next_point = TrackPoint(coord_list[idx + 1][0], coord_list[idx + 1][1])
        except IndexError:
            # Si nos hemos pasado con el indice apuntaremos directamente al final.
            print("Error de indice")
            next_point = segment_target_point

        bearing = origin_point.get_bearing(next_point)

        # Calculamos una desviación
        random_bearing = np.random.uniform(bearing - 20, bearing + 20)

        # Calculamos distacia al punto que queremos crear
        #point_distance = utils.get_random_value(track_analysis.trackpoint_distance) / 8000
        point_distance = 20

        # Generamos el punto
        generated_point = origin_point.generate_point(random_bearing, point_distance)
        generated_point_distance = geopy.distance.distance((generated_point.get_longlat()), (next_point.get_longlat())).m
        i = 0
        while generated_point_distance > 70 and i < 30:
            i = i + 1
            random_bearing = np.random.uniform(bearing - 20, bearing + 20)

            generated_point = origin_point.generate_point(random_bearing, point_distance)
            generated_point_distance = geopy.distance.distance((generated_point.get_longlat()), (next_point.get_longlat())).m

        # Calculamos la distancia entre este punto y el final
        aux = geopy.distance.distance((generated_point.get_longlat()), (segment_target_point.get_longlat())).m

        # Meter el punto en el segmento resultante
        segment.append((generated_point.get_longlat()))

        # Devolvemos el punto y la distancia de este al final
        return generated_point, aux



    def get_most_frequent_node(self, node, path):
        """
        Every segment have a frequency. It returns choose one of the options according the frequencies.
        :param path:
        :param node: Node of the selection
        :return: selected target node
        """
        target_list = [[i[1], i[2]['frequency']] for i in list(self.graph.get_edge_by_node(node))]
        target_list.sort(key=lambda x: x[1])
        target_node_list = [item[0] for item in target_list]
        target_prob_list = [item[1] for item in target_list]
        target_prob_list /= sum(target_prob_list)
        if round(sum(target_prob_list)) != 1:
            print(target_prob_list)
        selected_target = np.random.choice(target_node_list, 1, p=target_prob_list)
        return selected_target.item()

    def calculate_initial_compass_bearing(self, pointA, pointB):
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

    def get_closest_segment_point(self, coord_list, point):
        # Por cada elemento buscar la distancia.
        distances = [[x[0], x[1], utils.haversine_distance(TrackPoint(x[0], x[1]), TrackPoint(point))] for x in coord_list]

        # Ordenar por esta nueva columna y coger el primer elemento
        closest_element = sorted(distances, key=lambda x: x[2])[0]
        return coord_list.index((closest_element[0], closest_element[1]))

