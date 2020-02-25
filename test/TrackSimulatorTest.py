import unittest
from entities.TrackSimulator_impl import TrackSimulator
from repository.graph_repository_impl import GraphRepositoryImpl as GraphRepository
from repository.trackstatistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository


class MyTestCase(unittest.TestCase):
    def test_something(self):
        graph_repository = GraphRepository('localhost', 27017)
        statistics_repository = TrackStatisticsRepository('localhost', 27017)
        
        graph = 'graph'
        statistics = 'statistics'

        simulator = TrackSimulator(graph, statistics)




if __name__ == '__main__':
    unittest.main()
