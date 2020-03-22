from interactor.Simulator import Simulator
from entities.Graph_impl import Graph
from entities.TrackPoint import TrackPoint as Point

import numpy as np
import geopy
import geopy.distance
import utils


class TrackSimulator(Simulator):
    def __init__(self, graph: Graph):
        self.graph = graph

    def simulate(self, source_node, distance):
        #  TODO: Implement method
        #  For n-times, simulate track from the graph
        self.simulate_track(source_node, distance)

        pass

    def simulate_track(self, source_node, distance):
        #  Generate most posible track given frequent statistics
        path = self.get_most_frequent_track(source_node, distance)
        processed_path = [[[path[i]], path[i - 1]] for i in range(1, len(path))]
        #  Generate track
        track = self.simulate_track(processed_path)
        pass

    def simulate_track(self, path):
        track = []
        for segment in path:
            track = track + self.simulate_segment(segment)
        return track

    def simulate_segment(self, segment):
        origin_node = segment[0]
        target_node = segment[1]
        segment = []
        origin_point = Point(self.graph.get_nodes()[origin_node]['y'], self.graph.get_nodes()[origin_node]['x'])
        target_point = Point(self.graph.get_nodes()[target_node]['y'], self.graph.get_nodes()[target_node]['x'])
        try:
            dest, aux = self.calculate_point(segment, origin_node, target_node, origin_point, target_point)
            next = dest
            while aux > 24 and len(segment) < 30:
                dest, aux = self.calculate_point(segment, origin_node, target_node, next, target_point)
                next = dest
        except KeyError:
            pass
        return np.array(segment)

    def simulate_point(self, track_analysis, segment, origin_node, target_node, origin_point, target_point):

        # Cargar la estructura de lista del segmento
        coords = self.graph.get_edges(origin_node, target_node)['geometry'].coords[:]
        coord_list = [list(reversed(item)) for item in coords]

        # Calcular el indice del punto GPS más cercano del segmento
        idx = self.get_closest_segment_point(coord_list, origin_node, target_node, origin_point)

        # Calculamos la dirección entre el punto que origen y el siguiente punto encontrado
        try:
            destPoint = (coord_list[idx + 1][0], coord_list[idx + 1][1])

        except IndexError:
            print("Error de indice")
            destPoint = (target_point[0], target_point[1])
            # Si nos hemos pasado con el indice apuntaremos directamente al final.

        bearing = Point(origin_point[0], origin_point[1]).get_bearing(destPoint[1])

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


    def get_most_frequent_track(self, source_node, distance):
        #  Get most frequent next node
        track = []
        gen_distance = 0
        while gen_distance <= distance:
            next_node = self.graph.get_next_node(source_node)
            track.append(next_node)
        return track
