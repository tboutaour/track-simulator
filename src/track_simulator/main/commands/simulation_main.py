from track_simulator.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_simulator.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_simulator.repository.resource.pyplot_resource_impl import PyplotResourceImpl
from track_simulator.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_simulator.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
from track_simulator.entities.graph_impl import Graph
from track_simulator.interactor.simulate_track_impl import SimulateTrackImpl
from track_simulator.pipelines.track_simulator_pipeline import TrackSimulatorPipeline
from track_simulator.conf.config import LAST_VERSION_GRAPH
from track_simulator.conf.config import NORTH_COMPONENT, SOUTH_COMPONENT, EAST_COMPONENT, WEST_COMPONENT


def simulation_main(origin_lat, origin_lon, distance, data, quantity, north_component, south_component, east_component,
                    west_component):
    """
    Main function to deploy pipeline that simulates track based on previous analysis.

    :param origin_point: Point to start simulation.
    :param distance: Distance to start simulation.
    :param data: Data to import from database. (Graph_Analysis_mm-dd-YYYY)
    :param quantity: Number of tracks to generate.
    """
    if data is None:
        data = 'Graph_Analysis_05-24-2020'
    # Resource
    mongo_resource = MongoResourceImpl()
    pyplot_resource = PyplotResourceImpl()
    gpx_resource = GPXResourceImpl()

    # Repository
    graph_repository = GraphInformationRepositoryImpl(mongo_resource)
    track_statistics_repository = TrackStatisticsRepositoryImpl(mongo_resource)

    # Entity
    useDefaultZone = any(elem is None for elem in [north_component, south_component, east_component, west_component])
    if useDefaultZone:
        zone_graph = Graph(NORTH_COMPONENT, SOUTH_COMPONENT, EAST_COMPONENT, WEST_COMPONENT)
    else:
        zone_graph = Graph(north_component, south_component, east_component, west_component)

    zone_graph.load_graph_analysis_statistics(graph_repository.read_graph_information_dataframe(data))

    # Interactors
    simulate_track = SimulateTrackImpl(
        graph=zone_graph,
        number_simulations=4,
        gpx_resource=gpx_resource,
        pyplot_resource=pyplot_resource,
        track_statistics_repository=track_statistics_repository
    )

    # Pipeline
    track_simulator_pipeline = TrackSimulatorPipeline(simulate_track)

    # Run
    track_simulator_pipeline.run(
        origin_lat=float(origin_lat),
        origin_lon=float(origin_lon),
        distance=int(distance),
        quantity=int(quantity))
