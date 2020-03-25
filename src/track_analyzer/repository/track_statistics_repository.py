import abc


class TrackStatisticsRepository(abc.ABC):

    @abc.abstractmethod
    def read_track_statistics(self):
        pass

    def write_track_statistics(self):
        pass
