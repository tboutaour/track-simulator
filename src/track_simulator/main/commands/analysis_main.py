from track_simulator.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_simulator.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_simulator.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_simulator.repository.track_information_repository_impl import TrackInformationRepositoryImpl
from track_simulator.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
from track_simulator.entities.graph_impl import Graph
from track_simulator.interactor.get_map_matching_impl import GetMapMatchingImpl
from track_simulator.interactor.get_trackanalysis_dataframe_impl import GetTrackAnalysisDataframeImpl
from track_simulator.interactor.get_trackanalysis_statistics_impl import GetTrackAnalysisStatisticsImpl
from track_simulator.interactor.get_analysis_figure_impl import GetAnalysisFigureImpl
from track_simulator.interactor.get_trackanalysis_graph_impl import GetTrackAnalysisGraphImpl
from track_simulator.pipelines.track_analysis_pipeline import TrackAnalysisPipeline
from track_simulator.entities.hidden_markov_model_impl import HMM
from track_simulator.conf.config import NORTH_COMPONENT, SOUTH_COMPONENT, EAST_COMPONENT, WEST_COMPONENT


def analysis_main(file_directory, north_component, south_component, east_component, west_component):
    """
    Main function to deploy pipeline that analyzes GPX tracks in directory

    :param file_directory: directory path where files are stored.
    :param north_component: North component of limited area.
    :param south_component: South component of limited area.
    :param east_component: East component of limited area.
    :param west_component: West component of limited area.
    """
    # Resources
    gpx_resource = GPXResourceImpl()
    mongo_resource = MongoResourceImpl()

    # Repositories
    graph_information = GraphInformationRepositoryImpl(mongo_resource)
    track_information = TrackInformationRepositoryImpl(mongo_resource)
    track_statistics = TrackStatisticsRepositoryImpl(mongo_resource)

    # Entities
    useDefaultZone = any(elem is None for elem in [north_component, south_component, east_component, west_component])

    if useDefaultZone:
        zone_graph = Graph(NORTH_COMPONENT, SOUTH_COMPONENT, EAST_COMPONENT, WEST_COMPONENT)
    else:
        zone_graph = Graph(north_component, south_component, east_component, west_component)

    # Interactors
    get_map_matching = GetMapMatchingImpl(HMM(zone_graph))
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
                                                    graph=zone_graph)

    # Execution

    track_analyzer_pipeline.run(file_directory)