import abc
from pandas import DataFrame

class TrackStatisticsRepository(abc.ABC):

    @abc.abstractmethod
    def read_distance_point_projection(self):
        pass

    @abc.abstractmethod
    def read_distance_point_to_next(self):
        pass

    @abc.abstractmethod
    def write_track_statistics(self, id_track, data: DataFrame):
        pass

    @abc.abstractmethod
    def write_many_track_statistics(self, data):
        pass