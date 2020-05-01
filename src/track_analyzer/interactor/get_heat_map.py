import abc
from track_analyzer.entities.graph_impl import Graph

class GetHeatMap(abc.ABC):
    @abc.abstractmethod
    def apply(self, graph: Graph, data):
        pass
