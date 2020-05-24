import abc
from pandas import DataFrame

class TrackStatisticsRepository(abc.ABC):

    @abc.abstractmethod
    def read_distance_point_projection(self):
        """
        Method to read analysis of distance point-projection stored in resource.
        """
        pass

    @abc.abstractmethod
    def read_distance_point_to_next(self):
        """
        Method to read analysis of distance point-to-point stored in resource.
        """
        pass

    @abc.abstractmethod
    def write_track_statistics(self, id_track, data: DataFrame):
        """
        Method to store analysis of distance point-to-point and point-projection pair stored in resource.
        """
        pass

    @abc.abstractmethod
    def write_many_track_statistics(self, data):
        """
        Method to store multiple analysis of distance point-to-point and point-projection pair stored in resource.
        """
        pass