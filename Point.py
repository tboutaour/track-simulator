from shapely.geometry import Point
from shapely.geometry import LineString
import math


class Point(Point):

    def get_latitude(self):
        return self.x

    def get_longitude(self):
        return self.y

    def haversine_distance(self, other):
        """ Haversine formula to calculate the distance between two lat/long points on a sphere """
        radius = 6371.0  # FAA approved globe radius in km
        dlat = math.radians(other.get_latitude() - self.get_latitude())
        dlon = math.radians(other.get_longitude() - self.get_longitude())
        a = math.sin(dlat / 2.) * math.sin(dlat / 2.) + math.cos(math.radians(self.get_latitude())) \
            * math.cos(math.radians(other.get_latitude())) * math.sin(dlon / 2.) * math.sin(dlon / 2.)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d * 1000


class Segment(LineString):

    def get_points(self):
        return self.coords[:]

    def distance(self):
        distance = 0.0
        n_coords = len(self.coords) - 1
        for i in range(0, n_coords):
            point1 = Point(self.coords[i])
            point2 = Point(self.coords[i + 1])
            distance += point1.haversine_distance(point2)
        return distance

    def get_middle_point(self):
        return self.coords[len(self.coords) // 2]

    def add_point(self, other):
        new_coord = self.coords[:]
        new_coord.append(other)
        self._set_coords(new_coord)


if __name__ == "__main__":
    point = Point(2, 1)
    point_b = Point(4, 4)
    print(point.get_longitude())
    print(point.haversine_distance(point_b))

    segm = Segment([point, point_b])

    print(segm.get_points())
    print(segm.distance())
    segm.add_point(point)
    print(segm.get_points())
