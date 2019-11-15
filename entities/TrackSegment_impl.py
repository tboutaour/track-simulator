from entities.TrackPoint_impl import TrackPoint as Point
from entities.Segment import Segment
from shapely.geometry import LineString


class TrackSegment(Segment):

    def __init__(self, sequence):
        self.segment = LineString(sequence)

    def get_points(self):
        return self.segment.coords[:]

    def get_distance(self):
        distance = 0.0
        n_coords = len(self.segment.coords) - 1
        for i in range(0, n_coords):
            point1 = Point(self.get_points()[i][0], self.get_points()[i][1])
            point2 = Point(self.get_points()[i + 1][0], self.get_points()[i + 1][1])
            distance += point1.haversine_distance(point2)
        return distance

    def get_middle_point(self):
        return self.get_points()[len(self.get_points()) // 2]

    def add_point(self, other):
        new_coord = self.segment.coords[:]
        new_coord.append(other)
        self.segment = LineString(new_coord)
