import unittest
import osmnx as osmnx
import matplotlib.pyplot as plt
import utils
from interactor.TrackSimulator_impl import TrackSimulator
from entities.Graph_impl import Graph
from repository.GraphInformation_repository_impl import GraphInformationRepositoryImpl as GraphInformationRepository



class MyTestCase(unittest.TestCase):
    def test_path_creation(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_03152020"
        data = mongodbConnection.get_graphinformation_dataframe(id_track)

        #Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulator(bellver_graph, 0)

        path, distance = simulator.create_path(1248507104, 12000)
        print(path, distance)
        ec = ['b' if (u == 2503944129 and v == 1357504260) else 'r' for u, v, k in bellver_graph.graph.edges(keys=True)]
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='w', node_edgecolor='k', node_size=30,
                                node_zorder=3, edge_color=ec, edge_linewidth=3)
        fig, ax = osmnx.plot_graph_route(bellver_graph.graph, path, edge_color=ec)
        plt.show()

    def test_path_creation_with_heat_map(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_03152020"
        data = mongodbConnection.get_graphinformation_dataframe(id_track)

        #Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulator(bellver_graph, 0)

        ec = utils.get_node_colors_by_stat(bellver_graph.graph, data=data, criteria='num of detections')
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', edge_color=ec, edge_linewidth=2.5)
        plt.show()

if __name__ == '__main__':
    unittest.main()



