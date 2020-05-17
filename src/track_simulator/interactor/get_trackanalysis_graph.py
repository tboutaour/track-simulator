import abc

class GetTrackAnalysisGraph(abc.ABC):
    @abc.abstractmethod
    def apply(self, graph, main_df):
        """
        Method to reduced DataFrame of analyze and update frequencies of graph
        :param graph:
        :param main_df:
        """
        pass
