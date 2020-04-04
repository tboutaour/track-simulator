import unittest

import matplotlib.pyplot as plt
import osmnx as osmnx

import utils
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.entities.track_point import TrackPoint as Point
from track_analyzer.pipelines.track_simulator_pipeline import TrackSimulatorPipeline
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl as GraphInformationRepository


class MyTestCase(unittest.TestCase):
    def test_path_creation(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_03152020"
        data = mongodbConnection.read_graph_information_dataframe(id_track)

        #Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)

        path, distance = simulator.create_path(1248507104, 4000)
        print(path, distance)
        # ec = ['b' if (u == 2503944129 and v == 1357504260) else 'r' for u, v, k in bellver_graph.graph.edges(keys=True)]
        fig, ax = osmnx.plot_graph_route(bellver_graph.graph, path)
        plt.show()

    def test_path_creation_with_heat_map(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_03152020"
        data = mongodbConnection.read_graph_information_dataframe(id_track)

        #Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)

        ec = utils.get_node_colors_by_stat(bellver_graph.graph, data=data, criteria='num of detections')
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', edge_color=ec, edge_linewidth=2.5)
        plt.show()

    def test_get_closest_segment_point(self):
        coord_list = [(2.6149201, 39.5580067), (2.6142689, 39.5584694), (2.6140847, 39.5585311)]
        point = (2.6149201, 39.5580067)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)
        result = simulator.get_closest_segment_point(coord_list, point)
        assert(0 == result)
        point = (2.6149201, 39.5580066)
        result = simulator.get_closest_segment_point(coord_list, point)
        assert(0 == result)

    def test_calculate_point(self):
        segment = [1248507104, 293027796, 1248507094, 1248507104, 293027796, 1248507104, 293027796, 1248507104, 317813195, 317813354, 317813195, 317813354, 317813453, 1357490350, 317813453, 317813462, 317813485, 1342069005, 317813485, 1342069005, 1594898117, 317813511, 1594898117, 317813511, 317813546, 317813577, 317813546, 317813511, 1594898117, 1342069005, 1594916474, 1342069005]

        origin_node = 1248507104
        target_node = 293027796
        origin_point = Point(2.6235541, 39.5673438)
        target_point = Point(2.6240736, 39.5671071)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)
        generated_point = simulator.calculate_point(segment, origin_node, target_node, origin_point, target_point)
        print(generated_point[0])


    def test_simulate_segment(self):
        segment = [1248507104, 293027796, 1248507094, 1248507104, 293027796, 1248507104, 293027796, 1248507104, 317813195, 317813354, 317813195, 317813354, 317813453, 1357490350, 317813453, 317813462, 317813485, 1342069005, 317813485, 1342069005, 1594898117, 317813511, 1594898117, 317813511, 317813546, 317813577, 317813546, 317813511, 1594898117, 1342069005, 1594916474, 1342069005]
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)

        simulated_segment = simulator.simulate_segment(segment)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, fig_height=10, fig_width=10, show=False, close=False,)
        utils.plot_points(ax, simulated_segment, 'blue')
        plt.show()
        print(simulated_segment)

    def test_simulate_segments(self):
        segments = [1248507104, 293027796, 1248507094, 1248507104, 293027796, 1248507104, 293027796, 1248507104,
                   317813195, 317813354, 317813195, 317813354, 317813453, 1357490350, 317813453, 317813462,
                   317813485, 1342069005, 317813485, 1342069005, 1594898117, 317813511, 1594898117, 317813511,
                   317813546, 317813577, 317813546, 317813511, 1594898117, 1342069005, 1594916474, 1342069005]
        segment_list = [[segments[idx], segments[idx + 1]] for idx in range(len(segments) - 1)]

        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)
        simulated_track = [simulator.simulate_segment(s) for s in segment_list]
        printable = sum(simulated_track, [])


        fig, ax = osmnx.plot_graph(bellver_graph.graph, fig_height=10, fig_width=10, show=False, close=False, )
        utils.plot_points(ax, printable, 'blue')
        plt.show()


    def test_all(self):
        COLOURS = ["green", "blue", "purple", "pink", "orange", "yellow", "black"]
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        id_track = "Graph_Analysis_03152020"
        data = mongodbConnection.read_graph_information_dataframe(id_track)

        # Graph information load
        bellver_graph.load_graph_analysis_statistics(data)
        simulator = TrackSimulatorPipeline(bellver_graph, 0)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, fig_height=10, fig_width=10, show=False, close=False, )
        for i in COLOURS:
            path, distance = simulator.create_path(1248507104, 10000)

            segment_list = [[path[idx], path[idx + 1]] for idx in range(len(path) - 1)]

            simulated_track = [simulator.simulate_segment(s) for s in segment_list]
            printable = sum(simulated_track, [])
            utils.plot_points(ax, printable, i)
        plt.show()


if __name__ == '__main__':
    unittest.main()



