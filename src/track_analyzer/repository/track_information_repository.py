import abc

class TrackInformationRepository(abc.ABC):

    @abc.abstractmethod
    def get_trackinformation_dataframe(self):
        pass

    def write_trackinformation_dataframe(self, data):
        pass
