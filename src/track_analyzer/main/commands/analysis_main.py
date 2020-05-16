from track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_analyzer.repository.track_information_repository_impl import TrackInformationRepositoryImpl
from track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.get_map_matching_impl import GetMapMatchingImpl
from track_analyzer.interactor.get_trackanalysis_dataframe_impl import GetTrackAnalysisDataframeImpl
from track_analyzer.interactor.get_trackanalysis_statistics_impl import GetTrackAnalysisStatisticsImpl
from track_analyzer.interactor.get_analysis_figure_impl import GetAnalysisFigureImpl
from track_analyzer.interactor.get_trackanalysis_graph_impl import GetTrackAnalysisGraphImpl
from track_analyzer.pipelines.track_analysis_pipeline import TrackAnalysisPipeline
from track_analyzer.entities.hidden_markov_model_impl import HMM


def analysis_main(file_directory):
    # Resources
    gpx_resource = GPXResourceImpl()
    mongo_resource = MongoResourceImpl()

    # Repositories
    graph_information = GraphInformationRepositoryImpl(mongo_resource)
    track_information = TrackInformationRepositoryImpl(mongo_resource)
    track_statistics = TrackStatisticsRepositoryImpl(mongo_resource)

    # Entities
    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

    # Interactors
    get_map_matching = GetMapMatchingImpl(HMM(bellver_graph))
    get_track_analysis = GetTrackAnalysisDataframeImpl()
    get_track_statistics = GetTrackAnalysisStatisticsImpl()
    get_analysis_figure = GetAnalysisFigureImpl()
    get_track_graph = GetTrackAnalysisGraphImpl()

    # Pipeline
    track_analyzer_pipeline = TrackAnalysisPipeline(gpx_resource=gpx_resource,
                                                    graph_information_repository=graph_information,
                                                    track_information_repository=track_information,
                                                    track_statistics_repository=track_statistics,
                                                    get_map_matching=get_map_matching,
                                                    get_track_analysis_dataframe=get_track_analysis,
                                                    get_track_statitstics=get_track_statistics,
                                                    get_analysis_figure=get_analysis_figure,
                                                    get_track_graph=get_track_graph,
                                                    graph=bellver_graph)

    # Execution

    track_analyzer_pipeline.run(file_directory)


if __name__ == '__main__':
    analysis_main()
