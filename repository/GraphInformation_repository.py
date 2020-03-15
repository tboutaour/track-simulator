import abc

class GraphInformationRepository(abc.ABC):

    @abc.abstractmethod
    def get_graphinformation_dataframe(self, id_track):
        pass

    @abc.abstractmethod
    def write_graphinformation_dataframe(self, data):
        pass
