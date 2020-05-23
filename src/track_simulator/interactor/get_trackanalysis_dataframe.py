import abc
from pandas import DataFrame


class GetTrackAnalysisDataframe(abc.ABC):
    @abc.abstractmethod
    def apply(self, id_track, track, projection) -> DataFrame:
        """
        Method to get DataFrame from track and projection information.

        :param id_track: Id track to add as a row.
        :param track: Array of Point
        :param projection: Array of [Projection, Origin, Target]
        """
        pass
