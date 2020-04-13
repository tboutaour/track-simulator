import abc


class TrackInformationRepository(abc.ABC):

    @abc.abstractmethod
    def get_trackinformation_dataframe(self, id_track):
        pass

    @abc.abstractmethod
    def write_trackinformation_dataframe(self, id_track, data):
        pass

    @abc.abstractmethod
    def write_trackinformation_dataframes(self, data):
        pass

