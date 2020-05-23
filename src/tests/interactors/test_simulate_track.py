import logging
import os
import sys
import unittest
from unittest import mock

import matplotlib.pyplot as plt
import osmnx
import utils
from track_simulator.entities.graph_impl import Graph

from track_simulator.pipelines.track_simulator_pipeline import TrackSimulatorPipeline

k = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatorempty",
                                 "MONGO_GRAPH_INFORMATION_COLLECTION": 'graphDataframe',
                                 "MONGO_TRACK_INFORMATION_COLLECTION": 'trackDataframe',
                                 "ROOT_DIRECTORY": "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackSimulator",
                                 "FILE_DIRECTORY": "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackSimulator/src"
                                                   "/data/tracks_to_analysis",
                                 "EXPORT_ANALYSIS_IMAGES_FOLDER": "/Users/tonibous/Documents/1-UIB/TrabajoFinal"
                                                                  "/TrackSimulator/src/data/analysis",
                                 "EXPORT_SIMULATIONS_IMAGES_FOLDER": "/Users/tonibous/Documents/1-UIB/TrabajoFinal"
                                                                     "/TrackSimulator/src/data/simulation/images",
                                 "EXPORT_SIMULATIONS_GPX_FOLDER": "/Users/tonibous/Documents/1-UIB/TrabajoFinal"
                                                                  "/TrackSimulator/src/data/simulation/gpx",
                                 "PYTHONPATH": "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackSimulator/src/",
                                 "RUNPATH": "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackSimulator/src"
                                            "/track_simulator/main ",
                                 "LAST_VERSION_GRAPH": "Graph_Analysis_05-10-2020"
                                                       ""
                                 })
k.start()

from track_simulator.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_simulator.repository.resource.pyplot_resource_impl import PyplotResourceImpl
from track_simulator.repository.graph_information_repository_impl import \
    GraphInformationRepositoryImpl
from track_simulator.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_simulator.repository.track_statistics_repository import TrackStatisticsRepository
from track_simulator.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
from track_simulator.interactor.simulate_track_impl import SimulateTrackImpl

k.stop()


class MyTestCase(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    def test_path_creation(self):
        mongo_resource = MongoResourceImpl()
        graph_information = GraphInformationRepositoryImpl(mongo_resource)

        track_statistics_repository = TrackStatisticsRepositoryImpl(mongo_resource)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        gpx_resource = GPXResourceImpl()
        pyplot_resource = PyplotResourceImpl()
        id_track = "Graph_Analysis_05-03-2020"
        try:
            k.start()
            data = graph_information.read_graph_information_dataframe(os.environ.get('LAST_VERSION_GRAPH'))
            k.stop()
        except IndexError:
            logging.warning("NOT found in MongoDB")
            return

        simulate_track = SimulateTrackImpl(bellver_graph, 4, gpx_resource, pyplot_resource, track_statistics_repository)
        # Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(simulate_track)

        path = simulator.run(1248507104, 10000)
        a = [x[0] for x in path]
        print(path)
        # ec = ['b' if (u == 2503944129 and v == 1357504260) else 'r' for u, v, k in bellver_graph.graph.edges(keys=True)]
        # fig, ax = osmnx.plot_graph_route(bellver_graph.graph, a,
        #                                  bgcolor='k',
        #                                  node_color='black',
        #                                  edge_linewidth=1.5,
        #                                  edge_alpha=1,
        #                                  node_zorder=3)
        # plt.show()

    def test_mocked_path_creation(self):
        mongo_resource = MongoResourceImpl()
        track_statistics_repository = TrackStatisticsRepositoryImpl(mongo_resource)
        graph_information = GraphInformationRepositoryImpl(mongo_resource)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        gpx_resource = GPXResourceImpl()
        pyplot_resource = PyplotResourceImpl()
        try:
            k.start()
            data = graph_information.read_graph_information_dataframe(os.environ.get('LAST_VERSION_GRAPH'))
            k.stop()
        except IndexError:
            logging.warning("NOT found in MongoDB")
            return
        simulate_track = SimulateTrackImpl(bellver_graph, 4, gpx_resource, pyplot_resource, track_statistics_repository)
        # Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(simulate_track)

        path = simulator.run(1248507104, 10000)
        a = [x[0] for x in path]
        print(path)
        fig, ax = osmnx.plot_graph_route(bellver_graph.graph, a,
                                         bgcolor='k',
                                         node_color='black',
                                         edge_linewidth=1.5,
                                         edge_alpha=1,
                                         node_zorder=3)
        plt.show()

    @unittest.skip
    def test_path_creation_with_heat_map(self):
        mongo_resource = MongoResourceImpl()
        graph_information = GraphInformationRepositoryImpl(mongo_resource)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_04-13-2020"
        data = graph_information.read_graph_information_dataframe(id_track)
        bellver_graph.load_graph_analysis_statistics(data)

        ec = utils.get_node_colors_by_stat(data=data, criteria='num of detections')
        fig, ax = osmnx.plot_graph(bellver_graph.graph,
                                   node_color='black',
                                   edge_color=ec,
                                   bgcolor='k',
                                   edge_linewidth=1.5,
                                   edge_alpha=1,
                                   node_zorder=3
                                   )


if __name__ == '__main__':
    unittest.main()
