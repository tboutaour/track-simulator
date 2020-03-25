import unittest
import pandas as pd
from src.track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from src.track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl

class MyTestCase(unittest.TestCase):
    def test_writting(self):
        mongodb_connection = MongoResourceImpl()
        data = pd.read_csv('../../../graphDataframe.csv', index_col=0)

        graph_information_repository = GraphInformationRepositoryImpl(mongodb_connection)
        data = graph_information_repository.write_graph_information_dataframe('graphDataframe', data)
        print(data)
        self.assertEqual(True, True)

    def test_reading(self):
        mongodb_connection = MongoResourceImpl()
        graph_information_repository = GraphInformationRepositoryImpl(mongodb_connection)
        id_track = 'Graph_Analysis_03152020'
        data = graph_information_repository.read_graph_information_dataframe(id_track)
        print(data)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
