import unittest
from entities.HMMMapMatching_impl import MapMatching
from entities.HiddenMarkovModel_impl import HMM
from entities.GPXLoaderSaver_impl import GPXLoaderSaver as LoaderSaver
from entities.TrackSegment_impl import TrackSegment as Segment
from entities.TrackPoint_impl import TrackPoint as Point
from entities.Graph_impl import Graph
import matplotlib.pyplot as plt
import osmnx


class MyTestCase(unittest.TestCase):
    def test_file_reading_and_plotting(self):
        test_file = LoaderSaver("../tracks/Ficheros/rutasMFlores/activity_3276836874.gpx")
        parsed_file = test_file.parseFile()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)

        hidden_markov_model = HMM(graph=bellver_graph)
        map_matching = MapMatching(points=parsed_file, hmm=hidden_markov_model)

        mapped_points = map_matching.match()

        [ax.scatter(lon, lat, c='green', s=20) for lat, lon in parsed_file]
        [ax.scatter(lon, lat, c='blue', s=20) for lat, lon in mapped_points]
        plt.show(ax)
        [ax.scatter(lon, lat, c='red', s=20) for lat, lon in parsed_file]
        self.assertEqual(True, False)

    def test_get_nearest_segment_points(self):
        test_file = LoaderSaver("../tracks/Ficheros/rutasMFlores/activity_3276836874.gpx")
        point = Point(39.5586107, 2.6227118)
        parsed_file = test_file.parseFile()
        point = Point(parsed_file[120])
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
        for p in parsed_file:
            p = Point(p)
            list_of_points = hidden_markov_model.get_closest_nodes(Point(p))
            plt.scatter(p.get_longitude(),p.get_latitude(), c= "green" )
            for res in list_of_points:
                plt.scatter(Point(res).get_latitude(), Point(res).get_longitude(), c="red")
        plt.show()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
