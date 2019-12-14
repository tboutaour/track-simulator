import unittest
from entities.TrackAnalyzerStatistics_impl import TrackAnalyzerStatistics as Statistics
from entities.TrackPoint_impl import TrackPoint as Point
from entities.TrackSegment_impl import TrackSegment as Segment
from entities.Graph_impl import Graph
import numpy as np
import pandas as pd
import geopandas as gp


class MyTestCase(unittest.TestCase):
    def test_something(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)

        import_data = [[1, 2, 1, 2, 1248507104, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507105, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507106, 317813195], [1, 2, 1, 2, 1248507104, 317813195]]

        statistics = Statistics(bellver_graph, import_data)
        grouped = statistics.group_point_by_segment()
        print(grouped)
        self.assertIsInstance(statistics.dataset, pd.DataFrame)

    def test_reduce_track(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)

        import_data = [[1, 2, 1, 2, 1248507104, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507105, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507106, 317813195], [1, 2, 1, 2, 1248507104, 317813195]]

        expected_list = [[1, 2, 1, 2, 1248507104, 317813195], [1, 2, 1, 2, 1248507105, 317813195],
                         [1, 2, 1, 2, 1248507104, 317813195], [1, 2, 1, 2, 1248507106, 317813195],
                         [1, 2, 1, 2, 1248507104, 317813195]]

        expected_data = pd.DataFrame(expected_list,
                                     columns=['X_point', 'Y_point', 'X_projection', 'Y_projection', 'Origin', 'Target'])
        statistics = Statistics(bellver_graph, import_data)
        _ = statistics.group_point_by_segment()
        result = statistics.reduce_track()
        self.assertEqual(expected_data.equals(result), True)

    def test_get_point_projection_distance(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)

        import_data = [[1, 2, 1, 2, 1248507104, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507105, 317813195], [1, 2, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507106, 317813195], [1, 2, 1, 2, 1248507104, 317813195]]

        expected_list = [[1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507105, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507106, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))]]

        expected_data = pd.DataFrame(expected_list,
                                     columns=['X_point', 'Y_point', 'X_projection', 'Y_projection',
                                              'Origin', 'Target',
                                              'Point_projection_distance'])

        statistics = Statistics(bellver_graph, import_data)
        statistics.get_distance_point_projection()
        self.assertEqual(expected_data.equals(statistics.dataset), True)


    def test_get_point_point_distance(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)

        import_data = [[1, 2, 1, 2, 1248507104, 317813195], [3, 4, 1, 2, 1248507104, 317813195],
                       [5, 6, 1, 2, 1248507105, 317813195], [7, 8, 1, 2, 1248507104, 317813195],
                       [1, 2, 1, 2, 1248507106, 317813195], [1, 2, 1, 2, 1248507104, 317813195]]

        expected_list = [[1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507105, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507106, 317813195, Point(1, 2).distance(Point(1, 2))],
                         [1, 2, 1, 2, 1248507104, 317813195, Point(1, 2).distance(Point(1, 2))]]

        expected_data = pd.DataFrame(expected_list,
                                     columns=['X_point', 'Y_point', 'X_projection', 'Y_projection',
                                              'Origin', 'Target',
                                              'Point_projection_distance'])

        statistics = Statistics(bellver_graph, import_data)
        distance = statistics.get_distance_between_points()
        self.assertEqual(expected_data.equals(statistics.dataset), True)
    if __name__ == '__main__':
        unittest.main()
