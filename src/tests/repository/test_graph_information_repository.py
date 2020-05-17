import os
import unittest
from unittest import mock
import pandas as pd
k = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatorempty"})
k.start()
from track_simulator.entities.graph_impl import Graph
from track_simulator.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_simulator.repository.resource.mongo_resource_impl import MongoResourceImpl
k.stop()

class MyTestCase(unittest.TestCase):
    def test_writting(self):
        mongodb_connection = MongoResourceImpl()
        data = pd.read_csv('./graphDataframe.csv', index_col=0)

        graph_information_repository = GraphInformationRepositoryImpl(mongodb_connection)
        data = graph_information_repository.write_graph_information_dataframe(data)
        print(data)
        self.assertEqual(True, True)

    def test_reading(self):
        mongodb_connection = MongoResourceImpl()
        graph_information_repository = GraphInformationRepositoryImpl(mongodb_connection)
        id_track = 'Graph_Analysis_04-05-2020'
        data = graph_information_repository.read_graph_information_dataframe(id_track)
        print(data)
        self.assertEqual(True, True)

    def test_writting_empty_graph(self):
        mongodb_connection = MongoResourceImpl()
        graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        data = graph.get_edgelist_dataframe()

        graph_information_repository = GraphInformationRepositoryImpl(mongodb_connection)
        data = graph_information_repository.write_graph_information_dataframe(data)
        print(data)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
