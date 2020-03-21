import abc


class Point(abc.ABC):

    @abc.abstractmethod
    def get_latitude(self):
        pass

    @abc.abstractmethod
    def get_longitude(self):
        pass

    @abc.abstractmethod
    def get_latlong(self):
        pass

    @abc.abstractmethod
    def generate_point(self, bearing, distance):
        pass

    @abc.abstractmethod
    def get_bearing(self, point_b):
        pass


