import unittest
import matplotlib.pyplot as plt
import utils
from repository.trackstatistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatistics



class MyTestCase(unittest.TestCase):
    def test_something(self):
        mongodbConnection = TrackStatistics('localhost', 27017)
        data1 = [1, 3, 3, 4, 45]
        data2 = [2, 4, 6, 8, 10]
        mongodbConnection.write_track_statistics(1, data1, 0, data2, 0)
        self.assertEqual(True, True)

    def test_getting(self):
        mongodbConnection = TrackStatistics('localhost', 27017)
        d1, d2, ac1, ac2 = mongodbConnection.get_track_statistics()
        print(d1.get("data"))
        print(d2.get("data"))
        print(ac1.get("data"),ac1.get("datetime"))
        print(ac2.get("data"))
        _, ax1 = plt.subplots()
        utils.plot_histogram(d1.get("data"), ax1)

        _, ax2 = plt.subplots()
        utils.plot_histogram(d2.get("data"), ax2)

        utils.plot_accumultaive_distribution(d1.get("data"), ac1.get("data"))
        utils.plot_accumultaive_distribution(d2.get("data"), ac2.get("data"))
        plt.show()


if __name__ == '__main__':
    unittest.main()
