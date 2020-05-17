import abc
from pandas import DataFrame


class GetTrackAnalysisStatistics(abc.ABC):
    @abc.abstractmethod
    def apply(self, data: DataFrame) -> DataFrame:
        """
        Method to get statistics from DataFrame
        :param data: DataFrame with [Point_lat, Point_long, Projection_lat, Projection_lon, Origin, Target]
        """
        pass
