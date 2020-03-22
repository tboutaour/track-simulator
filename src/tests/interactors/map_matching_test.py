import unittest
from src.track_analyzer.interactor.hmm_map_matching_impl import MapMatching
from src.track_analyzer.entities.hidden_markov_model_impl import HMM
from src.track_analyzer.repository.gpx_track_repository_impl import GPXTrackRepositoryImpl as LoaderSaver
from src.track_analyzer.entities.track_point import TrackPoint as Point
from src.track_analyzer.entities.graph_impl import Graph
import matplotlib.pyplot as plt
import osmnx
import seaborn as sns; sns.set()


class MyTestCase(unittest.TestCase):
    def test_get_nearest_segment_points(self):
        test_file = LoaderSaver("../../../tracks/Ficheros/rutasMFlores/activity_3689734814.gpx")
        point = Point(39.5586107, 2.6227118)
        parsed_file = test_file.parseFile()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
        for p in parsed_file:
            list_of_points = hidden_markov_model.get_closest_nodes(p[2])
            plt.scatter(p[2].get_longitude(), p[2].get_latitude(), c="blue")
            plt.scatter(list_of_points[0][0].get_longitude(), list_of_points[0][0].get_latitude(), c="green")
            for res in range(2, len(list_of_points)):
                plt.scatter(list_of_points[res][0].get_longitude(), list_of_points[res][0].get_latitude(), c="red")

        plt.show()
        self.assertEqual(True, False)

    def test_viterbi_algorithm(self):
        test_file = LoaderSaver("../../../tracks/Ficheros/rutasMFlores/activity_3689734814.gpx")
        point = Point(2.6227118, 39.5586107)
        parsed_file = test_file.parseFile()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
        for p in parsed_file:
            plt.scatter(p[2].get_longitude(), p[2].get_latitude(), c="green")
        parsed_point_list = [x[2]for x in parsed_file]
        hmm = MapMatching(parsed_point_list, hidden_markov_model)
        result = hmm.match()
        for r in result:
            plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
            print(r)
        plt.show()
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
