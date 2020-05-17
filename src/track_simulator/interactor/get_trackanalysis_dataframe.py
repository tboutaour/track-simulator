import abc
from pandas import DataFrame


class GetTrackAnalysisDataframe(abc.ABC):
    @abc.abstractmethod
    def apply(self, id_track, track, projection):
        pass
