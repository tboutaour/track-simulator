import abc
import numpy as np
from Point import Point, Segment
import random
import geopy
import utils
NUMBER_SIMULATIONS = 4
PROB_RETURN = 0.4

class Simulator(abc.ABC):

    @abc.abstractmethod
    def simulate(self):
        """."""
        return


class TrackSimulator(Simulator):
    def simulate(self):
        pass

    def simulate_route(self,track_analysis, origin, end, distance, ax):
        """
        Simulates creation of route given an origin and target point.
        This simulation is made by searching Dijkstra's path and simulating points segment by segment.

        :param track_analysis: Object of TrackAnalyzer class
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
            simulated_path_aux, distance_generated = self.create_path(track_analysis, origin, distance)
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
            seg = self.simulate_segment(track_analysis, segment)
            idx_color = idx_color + 1
            for s in seg:
                simulated_track.append(s)

        return np.array(simulated_track), distance_to_return

    def simulate_segment(self, track_analyze, segment):
        """
        Simulates creation of points in the segment delimited by two nodes of the graph
        :param track_analyze: TrackAnalysis of the project with all the information for recreating the segment
        :param segment: Segment to simulate (Origin node, Target node)
        :return: Array of points (lat,lon) of the simulation
        """
        if track_analyze.trackpoint_number:
            gen_points_number = utils.get_random_value(track_analyze.trackpoint_number)
        else:
            gen_points_number = 12

        aux = 0
        origin_node = segment[0]
        target_node = segment[1]
        segment = []
        origin_point = Point(track_analyze.graph.nodes[origin_node]['y'], track_analyze.graph.nodes[origin_node]['x'])
        target_point = Point(track_analyze.graph.nodes[target_node]['y'], track_analyze.graph.nodes[target_node]['x'])
        #d = geopy.distance.distance(origin_point, target_point).m
        d = origin_point.haversine_distance(target_node)*1000

        try:
            dest, aux = self.calculate_point(track_analyze, segment, origin_node, target_node, origin_point, target_point)
            next = dest
            while aux > 24 and len(segment) < 30:
                dest, aux = self.calculate_point(track_analyze, segment, origin_node, target_node, next, target_point)
                next = dest
        except KeyError:
            pass
        return np.array(segment)

    def calculate_point(self, track_analysis, segment, origin_node, target_node, origin_point, target_point):
        """
        Calculates the point for the simulated segment.
        This point is calculated by a distance and a bearing.
        While the distance from the generated point to the closest point of the segment is not sustainable we recalculate
        the point.

        :param track_analysis: Object of TrackAnalyzer class
        :param segment: Segment related to the generated point
        :param origin_node: Origin node of the segment
        :param target_node: Target node of the segment
        :param origin_point: Origin GPS point of the segment
        :param target_point: Target point of the segment
        :return:
        """
        if track_analysis.trackpoint_route_distance:
            rnd_distance = random.choice(track_analysis.trackpoint_route_distance) / 1000
        else:
            rnd_distance = 0.04
        rnd_distance = 0.04
        # Cargar la estructura de lista del segmento
        coords = track_analysis.graph.edges[(origin_node, target_node, 0)]['geometry'].coords[:]
        coord_list = [list(reversed(item)) for item in coords]

        # Calcular el indice del punto GPS más cercano del segmento
        idx = track_analysis.get_closest_segment_point(track_analysis, coord_list, origin_node, target_node, origin_point)
        # print("indice del punto más cercano: " + str(idx))

        # Calculamos la dirección entre el punto que origen y el siguiente punto encontrado
        try:
            destPoint = (coord_list[idx + 1][0], coord_list[idx + 1][1])

        except IndexError:
            print("Error de indice")
            destPoint = (target_point[0], target_point[1])
            # Si nos hemos pasado con el indice apuntaremos directamente al final.

        bearing = Point(origin_point[0], origin_point[1]).calculate_initial_compass_bearing(destPoint[0], destPoint[1])

        # Calculamos una desviación
        rndbear = np.random.uniform(bearing - 20, bearing + 20)

        # Calculamos distacia al punto que queremos crear
        point_distance = utils.get_random_value(track_analysis.trackpoint_distance) / 8000
        # point_distance = rnd_distance

        # Generamos el punto
        dest = Point(origin_point[0], origin_point[1]).generate_point(rndbear, point_distance)

        dist_gen_point = geopy.distance.distance(dest, (destPoint[0], destPoint[1])).m
        i = 0
        while dist_gen_point > 70 and i < 30:
            i = i + 1
            rndbear = np.random.uniform(bearing - 20, bearing + 20)

            dest = Point(origin_point[0], origin_point[1]).generate_point(rndbear, point_distance)
            dist_gen_point = geopy.distance.distance(dest, (destPoint[0], destPoint[1])).m

        # Calculamos la distancia entre este punto y el final
        aux = geopy.distance.distance(dest, target_point).m

        # Meter el punto en el segmento resultante
        segment.append(Point(dest[0], dest[1]))

        # Devolvemos el punto y la distancia de este al final
        return dest, aux

    def create_path(self,track_analysis, origin, dist):
        """
        Create the most frequent path given frequencies stored at track_analysis object.
        Given an origin node and a maximum distance it creates the most frequent path.
        Once the track_analysis is updated the path may change.
        It does not recognise returns of route.
        :param track_analysis:  Object of TrackAnalyzer class
        :param origin: Origin node of the simulated route
        :param dist: Distance of the route.
        :return: created path, distance of this path.
        """
        path = []
        distance_created = 0
        prev_node = origin
        path.append(origin)
        while distance_created < dist:
            next_node = self.get_most_frequent_node(track_analysis, prev_node, path)
            distance_aux = distance_created + track_analysis.graph.edges[(prev_node, next_node, 0)]['length']
            if distance_aux < dist:
                distance_created = distance_aux
                path.append(next_node)
                prev_node = next_node
            else:
                return path, distance_created
        return path, distance_created

    def get_most_frequent_node(self, track_analysis, node, path):
        """
        Every segment have a frequency. It returns choose one of the options according the frequencies.
        :param path:
        :param track_analysis: Object od TrackAnalyzer class
        :param node: Node of the selection
        :return: selected target node
        """
        target_list = []
        roll = random.random()
        for i in track_analysis.graph.edges(node, data=True):
            target_list.append([i[1], i[2]['frequency']])
        target_list.sort(key=lambda x: x[1])
        aux = 0
        selected_target = 67
        idx_target = 0
        for target in target_list:

            aux = aux + target[1]
            if roll < aux:
                selected_target = target[0]
                if track_analysis.graph.degree(selected_target) > 1 and len(path) > 2 and path[-2] == selected_target:
                    retro_roll = random.random()
                    if retro_roll < PROB_RETURN:
                        selected_target = target[0]
                    else:
                        selected_target = target_list[idx_target - 1][0]
                break
            idx_target = idx_target + 1
        return selected_target
