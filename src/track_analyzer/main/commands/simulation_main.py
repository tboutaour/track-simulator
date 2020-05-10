from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_analyzer.repository.resource.pyplot_resource_impl import PyplotResourceImpl
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.simulate_track_impl import SimulateTrackImpl
from track_analyzer.pipelines.track_simulator_pipeline import TrackSimulatorPipeline
from track_analyzer.conf.config import LAST_VERSION_GRAPH




def simulation_main(origin_node, distance):
    origin_node = 1248507104  # Bellver Castle entrance
    distance = 20000  # In meters
    # Resource
    mongo_resource = MongoResourceImpl()
    pyplot_resource = PyplotResourceImpl()
    gpx_resource = GPXResourceImpl()
    # Repository
    graph_repository = GraphInformationRepositoryImpl(mongo_resource)
    track_statistics_repository = TrackStatisticsRepositoryImpl(mongo_resource)

    # Entity
    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    bellver_graph.load_graph_analysis_statistics(graph_repository.read_graph_information_dataframe(LAST_VERSION_GRAPH))

    # Interactors
    simulate_track = SimulateTrackImpl(bellver_graph, 4, gpx_resource, pyplot_resource, track_statistics_repository)

    # Pipeline
    track_simulator_pipeline = TrackSimulatorPipeline(simulate_track)

    # Run
    track_simulator_pipeline.run(origin_node, distance)


if __name__ == '__main__':
    simulation_main()
