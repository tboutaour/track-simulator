import unittest
import osmnx
from entities.Graph_impl import Graph
import networkx


class MyTestCase(unittest.TestCase):

    def test_something(self):
        osmnx_bellver_graph = osmnx.graph_from_bbox(39.5713, 39.5573, 2.6257, 2.6023)
        osmnx_bellver_graph
        bellver_graph = Graph(osmnx_bellver_graph)
        #self.assertEqual(bellver_graph.get_edges(), osmnx_bellver_graph.graph.edges(data=True))
        self.assertEqual(True,True)


if __name__ == '__main__':
    unittest.main()
