import unittest
from interactor.TrackSimulator_impl import TrackSimulator
from repository.Trackstatistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository


class MyTestCase(unittest.TestCase):
    def test_something(self):
        statistics_repository = TrackStatisticsRepository('localhost', 27017)

        graph = 'graph'
        statistics = 'statistics'

        simulator = TrackSimulator(graph, statistics)




if __name__ == '__main__':
    unittest.main()
