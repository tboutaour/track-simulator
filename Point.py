from shapely.geometry import Point
from shapely.geometry import LineString
import math


EARTH_RADIUM = 6378.1  # Radius of the Earth

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

    def generate_point(self, bearing, distance):
        bearing_radians = math.radians(bearing)

        lat_point = math.radians(point[0])  # Current lat point converted to radians
        lon_point = math.radians(point[1])  # Current long point converted to radians

        lat_result = math.asin(math.sin(lat_point) * math.cos(distance / EARTH_RADIUM) +
                               math.cos(lat_point) * math.sin(distance / EARTH_RADIUM) * math.cos(bearing_radians))

        lon_result = lon_point + math.atan2(math.sin(bearing_radians) * math.sin(distance / EARTH_RADIUM) *
                                            math.cos(lat_point),
                                            math.cos(distance / EARTH_RADIUM) - math.sin(lat_point) *
                                            math.sin(lat_result))

        lat_result = math.degrees(lat_result)
        lon_result = math.degrees(lon_result)

        return Point(lat_result,lon_result)

    def calculate_initial_compass_bearing(self, target_point):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
        if (type(self) != Point) or (type(target_point) != Point):
            raise TypeError("Only Point are supported as arguments")

        lat1 = math.radians(self.get_latitude())
        lat2 = math.radians(target_point.get_latitude())

        diff_long = math.radians(target_point.get_longitude() - self.get_longitude())

        x = math.sin(diff_long) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                               * math.cos(lat2) * math.cos(diff_long))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing


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
