import abc
from pandas import DataFrame
from track_simulator.entities.graph_impl import Graph


class GetHeatMap(abc.ABC):
    @abc.abstractmethod
    def apply(self, graph: Graph, data: DataFrame):
        """
        Method to get heatMap given a graph and data of edge frequencies.

        :param graph: Graph element
        :param data: Dataframe of graph with frequencies.
        """
        pass
