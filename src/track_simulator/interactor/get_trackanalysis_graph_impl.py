from track_simulator.interactor.get_trackanalysis_graph import GetTrackAnalysisGraph


class GetTrackAnalysisGraphImpl(GetTrackAnalysisGraph):
    def apply(self, graph, main_df):
        reduced_track = self.__reduce_track(main_df)
        reduced_track.apply(lambda x: graph.update_edge_freq(x.Origin, x.Target), axis=1)
        return graph

    def __reduce_track(self, dataset):
        data = (dataset.loc[dataset.Origin.shift() != dataset.Origin]).reset_index(drop=True)
        data.drop(data.tail(1).index, inplace=True)
        return data

