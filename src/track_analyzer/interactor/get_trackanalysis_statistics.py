import abc
from pandas import DataFrame


class GetTrackAnalysisStatistics(abc.ABC):
    @abc.abstractmethod
    def apply(self, data: DataFrame) -> DataFrame:
        pass