import unittest

import matplotlib.pyplot as plt
import osmnx
import utils
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.simulate_track_impl import SimulateTrackImpl
from track_analyzer.pipelines.track_simulator_pipeline import TrackSimulatorPipeline
from track_analyzer.repository.graph_information_repository_impl import \
    GraphInformationRepositoryImpl
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl


class MyTestCase(unittest.TestCase):
    @unittest.skip
    def test_path_creation(self):
        mongo_resource = MongoResourceImpl()
        graph_information = GraphInformationRepositoryImpl(mongo_resource)
        track_statistics_repository = TrackStatisticsRepositoryImpl(mongo_resource)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_04-13-2020"
        data = graph_information.read_graph_information_dataframe(id_track)

        simulate_track = SimulateTrackImpl(bellver_graph, 4, track_statistics_repository)
        # Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(simulate_track)

        path = simulator.run(1248507104, 7000)
        a = [x[0] for x in path]
        print(path)
        # ec = ['b' if (u == 2503944129 and v == 1357504260) else 'r' for u, v, k in bellver_graph.graph.edges(keys=True)]
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
