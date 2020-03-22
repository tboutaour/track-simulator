from entities.TrackPoint import TrackPoint as Point
from shapely.geometry import LineString, MultiPoint
from shapely.ops import nearest_points


class TrackSegment(LineString):
    def get_points(self):
        return self.coords[:]

    def get_distance(self):
        distance = 0.0
        n_coords = len(self.coords) - 1
        for i in range(0, n_coords):
            point1 = Point(self.get_points()[i][0], self.get_points()[i][1])
            point2 = Point(self.get_points()[i + 1][0], self.get_points()[i + 1][1])
            distance += point1.haversine_distance(point2)
        return distance

    def get_middle_point(self):
        return self.get_points()[len(self.get_points()) // 2]

    def add_point(self, other):
        new_coord = self.get_points()
        new_coord.append(other)
        return TrackSegment(new_coord)

    def get_nearest_point_from_segment(self, point: [Point]):
        #line_interpolate_point(linestring, line_locate_point(LineString, Point))
        #return self.interpolate(self.project(point))
        reversed_segment = TrackSegment([Point(track_point) for track_point in self.get_points()])
        return Point(nearest_points(reversed_segment, point)[0].coords)