import abc

class GraphRepository(abc.ABC):

    @abc.abstractmethod
    def get_graph(self, id_graph):
        pass

    def write_graph(self, graph):
        pass