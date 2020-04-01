import unittest
import pandas as pd
from src.track_analyzer.entities.graph_impl import Graph
from src.track_analyzer.entities.track_analyzer_statistics_impl import TrackAnalyzerStatistics as Statistics
from src.track_analyzer.entities.track_point import TrackPoint as Point


class MyTestCase(unittest.TestCase):
    def test_something(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        import_data = pd.DataFrame([[Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507105, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507106, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195]], columns=['Point', 'Projection', 'Origin', 'Target'])

        statistics = Statistics(bellver_graph, import_data)
        grouped = statistics.group_point_by_segment()
        print(grouped)
        self.assertIsInstance(statistics.dataset, pd.DataFrame)

    def test_reduce_track(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        import_data = pd.DataFrame([[Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507105, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507106, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195]], columns=['Point', 'Projection', 'Origin', 'Target'])

        expected_list = [[Point(1, 2), Point(1, 2), 1248507104, 317813195],
                         [Point(1, 2), Point(1, 2), 1248507105, 317813195],
                         [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                         [Point(1, 2), Point(1, 2), 1248507106, 317813195],
                         [Point(1, 2), Point(1, 2), 1248507104, 317813195]]

        expected_data = pd.DataFrame(expected_list,
                                     columns=['Point', 'Projection',
                                              'Origin', 'Target'])
        statistics = Statistics(bellver_graph, import_data)
        _ = statistics.group_point_by_segment()
        result = statistics.reduce_track()
        self.assertEqual(pd.testing.assert_frame_equal(expected_data, result, check_dtype=False), True)

    def test_get_point_projection_distance(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        import_data = pd.DataFrame([[Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507105, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507106, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195]], columns=['Point', 'Projection', 'Origin', 'Target'])

        expected_list = [[Point(1, 2), Point(1, 2), 1248507104, 317813195, Point(1, 2).haversine_distance(Point(1, 2))],
                         [Point(1, 2), Point(1, 2), 1248507104, 317813195, Point(1, 2).haversine_distance(Point(1, 2))],
                         [Point(1, 2), Point(1, 2), 1248507105, 317813195, Point(1, 2).haversine_distance(Point(1, 2))],
                         [Point(1, 2), Point(1, 2), 1248507104, 317813195, Point(1, 2).haversine_distance(Point(1, 2))],
                         [Point(1, 2), Point(1, 2), 1248507106, 317813195, Point(1, 2).haversine_distance(Point(1, 2))],
                         [Point(1, 2), Point(1, 2), 1248507104, 317813195, Point(1, 2).haversine_distance(Point(1, 2))]]

        expected_data = pd.DataFrame(expected_list,
                                     columns=['Point', 'Projection',
                                              'Origin', 'Target',
                                              'Point_projection_distance'])

        statistics = Statistics(bellver_graph, import_data)
        statistics.get_distance_point_projection()
        self.assertEqual(expected_data.equals(statistics.dataset), True)

    def test_get_point_point_distance(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

        import_data = pd.DataFrame([[Point(1, 2), Point(1, 2), 1248507104, 317813195],
                       [Point(3, 4), Point(1, 2), 1248507104, 317813195],
                       [Point(5, 6), Point(1, 2), 1248507105, 317813195],
                       [Point(7, 8), Point(1, 2), 1248507104, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507106, 317813195],
                       [Point(1, 2), Point(1, 2), 1248507104, 317813195]], columns=['Point', 'Projection', 'Origin', 'Target'])

        statistics = Statistics(bellver_graph, import_data)
        distance, _ = statistics.get_distance_between_points()
        expected_distance = [Point(1, 2).haversine_distance(Point(3, 4)),
                             Point(3, 4).haversine_distance(Point(5, 6)),
                             Point(5, 6).haversine_distance(Point(7, 8)),
                             Point(7, 8).haversine_distance(Point(1, 2)),
                             Point(1, 2).haversine_distance(Point(1, 2))]

        print(distance)
        print(expected_distance)
        self.assertEqual((len(distance) == len(expected_distance) and sorted(distance) == sorted(expected_distance)), True)

    if __name__ == '__main__':
        unittest.main()
