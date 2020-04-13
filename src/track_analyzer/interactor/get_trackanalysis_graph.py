import abc


class GetTrackAnalysisGraph(abc.ABC):
    @abc.abstractmethod
    def apply(self, graph, main_df):
        pass
