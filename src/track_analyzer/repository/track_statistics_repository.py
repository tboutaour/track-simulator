import abc


class TrackStatisticsRepository(abc.ABC):

    @abc.abstractmethod
    def get_track_statistics(self):
        pass

    def write_track_statistics(self,
                               id_track,
                               distance_point_projection,
                               distance_between_points, ):
        pass
