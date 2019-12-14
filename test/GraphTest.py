import unittest
import osmnx
import networkx
import pandas
from entities.Graph_impl import Graph
from entities.TrackSegment_impl import TrackSegment as Segment


class MyTestCase(unittest.TestCase):
    def test_something(self):
        osmnx_bellver_graph = osmnx.graph_from_bbox(39.5713, 39.5573, 2.6257, 2.6023)
        expected_edges = osmnx_bellver_graph.edges(data=True)
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023, Segment)
        edges = bellver_graph.get_edges()

        self.assertEqual(type(edges), type(expected_edges))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
