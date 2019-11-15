import abc


class Segment(abc.ABC):
    @abc.abstractmethod
    def get_points(self):
        pass

    @abc.abstractmethod
    def get_distance(self):
        pass

    @abc.abstractmethod
    def get_middle_point(self):
        pass

    @abc.abstractmethod
    def add_point(self, other):
        pass
