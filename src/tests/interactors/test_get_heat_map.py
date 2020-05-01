import os
import unittest
from unittest import mock

import matplotlib.pyplot as plt
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.get_heat_map_impl import GetHeatMapImpl

k = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatordb2"})
k.start()
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl
k.stop()


class MyTestCase(unittest.TestCase):

    def test_heat_map(self):
        print(os.path.abspath(os.curdir))
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
