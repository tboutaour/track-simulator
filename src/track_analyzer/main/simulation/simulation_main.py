from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.simulate_track_impl import SimulateTrackImpl
from track_analyzer.pipelines.track_simulator_pipeline import TrackSimulatorPipeline
from track_analyzer.main.simulation.arguments import Arguments

LAST_VERSION_GRAPH = "Graph_Analysis_03152020"


def simulation_main():
    #Args
    args = Arguments()
    origin = 1248507104  # Bellver Castle entrance
    distance = 10000  # In meters

    # Resource
    mongo_resource = MongoResourceImpl()

    # Repository
    graph_repository = GraphInformationRepositoryImpl(mongo_resource)

    # Entity
    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    bellver_graph.load_graph_analysis_statistics(graph_repository.read_graph_information_dataframe(LAST_VERSION_GRAPH))

    # Interactors
    simulate_track = SimulateTrackImpl(bellver_graph, 4)

    # Pipeline
    track_simulator_pipeline = TrackSimulatorPipeline(simulate_track)

    # Run
    track_simulator_pipeline.run(args.get_origin_node(), args.get_distance())


if __name__ == '__main__':
    simulation_main()
