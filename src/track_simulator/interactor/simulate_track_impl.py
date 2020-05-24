from track_simulator.interactor.simulate_track import SimulateTrack
from track_simulator.repository.resource.gpx_resource import GPXResource
from track_simulator.repository.resource.pyplot_resource import PyplotResource
from track_simulator.repository.track_statistics_repository import TrackStatisticsRepository
import math
import uuid
import pandas as pd
import geopy
import geopy.distance
import matplotlib.pyplot as plt
import numpy as np
import utils
from track_simulator.entities.graph import Graph
from track_simulator.entities.track_point import TrackPoint
from track_simulator.conf.config import GENERATION_DISTANCE
from track_simulator.conf.config import DESTINATION_NODE_THRESHOLD

COLORS = ["green", "red", "blue", "purple", "pink", "orange", "yellow", "black"]
DISTANCE_TO_FINAL_NODE = 24


def get_closest_segment_point(coord_list, point):
    """
    Get closest point of a list of points.
    :param coord_list: list of points
    :param point: original point to get the projection
    :return: closest point's index in list
    """
    # Search distance for each point
    distances = [[x[0], x[1], TrackPoint(x[0], x[1]).haversine_distance(TrackPoint(point))] for x in
                 coord_list]

    # Get first element given sorted list
    closest_element = sorted(distances, key=lambda x: x[2])[0]
    return coord_list.index((closest_element[0], closest_element[1]))


def get_random_value(ac_serie):
    rnd = np.random.random()
    return np.argmax(ac_serie > rnd)


class SimulateTrackImpl(SimulateTrack):
    def __init__(self, graph: Graph,
                 number_simulations,
                 gpx_resource: GPXResource,
                 pyplot_resource: PyplotResource,
                 track_statistics_repository: TrackStatisticsRepository):
        self.number_simulations = number_simulations
        self.graph = graph
        self.gpx_resource = gpx_resource
        self.pyplot_resource = pyplot_resource
        self.accumulative_point_distance_distribution = utils.get_cumulative_distribution(
            track_statistics_repository.read_distance_point_to_next(), 40)

    def simulate(self, origin_node: int, distance: int):
        print(DESTINATION_NODE_THRESHOLD)
        print(GENERATION_DISTANCE)
        simulated_track = []
        # Simular creación de trayectoria completa

        # Encontrar el camino más probable.
        list_original = []
        list_distances = []
        list_reduced = []

        # Realizamos 5 y nos quedamos con el que tenga menos repeticiones.
        for i in range(0, self.number_simulations):
            simulated_path_aux, distance_generated = self.create_path(origin_node, distance)
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

        #  para crear segmentos de colores distintos
        for segment in path:
            seg = self.simulate_segment(segment)
            for s in seg:
                simulated_track.append(s)
        generated_uid = str(uuid.uuid4())

        self.gpx_resource.write(generated_uid, simulated_track)
        self.pyplot_resource.write(generated_uid, self.graph, simulated_track)

        return path

    def create_path(self, origin, dist):
        """
        Path creation given origin and distance.
        :param origin: Origin node.
        :type origin: int
        :param dist: path distance in meters.
        :param dist: int
        :return:
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
        """
        Creates a simulation of points related to a segment.
        :param segment: Element [origin node, dest. node] to simulate
        :return: List of points related to the segment.
        """
        aux = 0
        origin_node = segment[0]
        target_node = segment[1]
        segment = []
        origin_point = TrackPoint(self.graph.get_nodes()[origin_node]['x'], self.graph.get_nodes()[origin_node]['y'])
        target_point = TrackPoint(self.graph.get_nodes()[target_node]['x'], self.graph.get_nodes()[target_node]['y'])
        try:
            dest, aux = self.calculate_point(segment, origin_node, target_node, origin_point, target_point)
            next = dest
            while aux > DESTINATION_NODE_THRESHOLD:
                dest, aux = self.calculate_point(segment, origin_node, target_node, next, target_point)
                next = dest
        except KeyError:
            pass
        return segment

    def calculate_point(self, segment, origin_node, target_node, origin_point: TrackPoint,
                        segment_target_point: TrackPoint):
        """
        Generation of point in a determinated segment. This function modifies segment
        adding simulated point.
        :param segment: [origin segment node, target segment node]
        :param origin_node: origin node from generate new point
        :param target_node: target node from generate new point
        :param origin_point: origin point from generation start
        :param segment_target_point: segment end point projection if
        :return: generated point.
        """
        # Load segment list structure
        coords = self.graph.get_edge_by_nodes(origin_node, target_node)['geometry'].coords[:]
        coord_list = [tuple(item) for item in coords]

        # Get closest point
        idx = get_closest_segment_point(coord_list, origin_point)

        # Get bearing origin point to destiny
        try:
            next_point = TrackPoint(coord_list[idx + 1][0], coord_list[idx + 1][1])
        except IndexError:
            # If point is out, directly point to last segment point
            next_point = segment_target_point

        bearing = origin_point.get_bearing(next_point)

        # Get bearing given deviation
        random_bearing = np.random.uniform(bearing - 20, bearing + 20)

        # Get distance from last point given analysis.
        if len(self.accumulative_point_distance_distribution) > 0:
            point_distance = get_random_value(self.accumulative_point_distance_distribution)
        else:
            point_distance = GENERATION_DISTANCE

        # Point generation
        generated_point = origin_point.generate_point(random_bearing, point_distance)
        generated_point_distance = geopy.distance.distance((generated_point.get_longlat()),
                                                           (next_point.get_longlat())).m
        i = 0
        while generated_point_distance > 70 and i < 30:
            i = i + 1
            random_bearing = np.random.uniform(bearing - 20, bearing + 20)

            generated_point = origin_point.generate_point(random_bearing, point_distance)
            generated_point_distance = geopy.distance.distance((generated_point.get_longlat()),
                                                               (next_point.get_longlat())).m

        # Get distance to final point
        aux = geopy.distance.distance((generated_point.get_longlat()), (segment_target_point.get_longlat())).m

        # Set last point
        segment.append((generated_point.get_longlat()))

        return generated_point, aux

    def get_most_frequent_node(self, node, path):
        """
        Get frequent segment node given a probability distribution in graph.
        :param node: node to select new segment.
        :param path: created path in order to detect recullation
        :return:
        """
        target_list = [[i[1], i[2]['frequency']] for i in list(self.graph.get_edge_by_node(node))]
        try:
            if len(path) > 1:
                target_list = [[i[0], i[1] * 0.002] if i[0] == path[-1] else i for i in target_list]
        except Exception:
            target_list = target_list
        target_list.sort(key=lambda x: x[1])
        target_node_list = np.array([item[0] for item in target_list])
        target_prob_list = np.array([item[1] for item in target_list])
        try:
            target_prob_list /= sum(target_prob_list)
        except TypeError:
            print(target_prob_list)
            print(sum(target_prob_list))
        if round(sum(target_prob_list)) != 1:
            print(target_prob_list)
        selected_target = np.random.choice(target_node_list, 1, p=target_prob_list)
        return selected_target.item()
