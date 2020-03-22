import unittest
import pandas as pd
from src.track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl as GraphInformationRepository


class MyTestCase(unittest.TestCase):
    def test_writting(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        data = pd.read_csv('../../../graphDataframe.csv', index_col=0)

        data = mongodbConnection.write_graphinformation_dataframe(data)
        print(data)
        self.assertEqual(True, True)

    def test_reading(self):
        mongodbConnection = GraphInformationRepository('localhost', 27019)
        id_track = "Graph_Analysis_03122020"
        data = mongodbConnection.get_graphinformation_dataframe(id_track)
        print(data)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
