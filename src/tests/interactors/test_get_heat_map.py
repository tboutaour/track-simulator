import unittest
from track_analyzer.interactor.get_heat_map_impl import GetHeatMapImpl
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
from track_analyzer.entities.graph_impl import Graph
import networkx
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_heat_map(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        get_heat_map = GetHeatMapImpl()
        mongo_resource = MongoResourceImpl()
        graph_information = GraphInformationRepositoryImpl(mongo_resource)
        id_graph = "Graph_Analysis_04-13-2020"
        data = graph_information.read_graph_information_dataframe(id_graph)
        # data['num of detections'] = data['num of detections'].apply(lambda x: 0 if x == 1 else x)
        bellver_graph.load_graph_analysis_statistics(data)
        get_heat_map.apply(bellver_graph, data)

        plt.show()
