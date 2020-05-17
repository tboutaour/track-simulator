import abc

class GraphInformationRepository(abc.ABC):

    @abc.abstractmethod
    def read_graph_information_dataframe(self, id_track):
        pass

    @abc.abstractmethod
    def write_graph_information_dataframe(self, data):
        pass
