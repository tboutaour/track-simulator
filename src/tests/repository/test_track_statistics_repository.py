import unittest
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MyTestCase(unittest.TestCase):
    def test_read_point_projection(self):
        mongodb_connection = MongoResourceImpl()
        track_information_repository = TrackStatisticsRepositoryImpl(mongodb_connection)
        data = track_information_repository.read_distance_point_projection()
        print(data)
        dx2 = data
        # Generación distribucion acumulada
        dx2.sort()
        out_threshold = 40.0
        net_dx2 = [i for i in dx2 if i < out_threshold]
        net_dx2 = np.array(net_dx2)
        net_dx2 = np.sort(net_dx2)
        cd_dx = np.linspace(0., 1., len(net_dx2))
        ser_dx = pd.Series(cd_dx, index=net_dx2)
        print(ser_dx)
        # plot
        plt.figure(figsize=(7, 8))
        plt.subplot(211)
        ser_dx.plot(drawstyle='default', legend="True", color='green')
        plt.xlabel("Meters")
        plt.ylabel("Frequency")
        plt.title("Cumulative distribution of distance point to projection")
        plt.legend().set_visible(False)
        plt.grid(True)
        plt.subplot(212)
        plt.hist(net_dx2, bins=300, alpha=0.5, color='green')
        plt.xlabel('Distance point to point')
        plt.ylabel('Frequency')
        plt.title('Histogram of distance point to projection')
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                            wspace=0.35)
        plt.show()
        # plt.savefig('distDist.eps', format='eps', dpi=600)
        self.assertEqual(True, True)

        self.assertEqual(True, True)

    def test_read_point_to_next(self):
        mongodb_connection = MongoResourceImpl()
        track_information_repository = TrackStatisticsRepositoryImpl(mongodb_connection)
        data = track_information_repository.read_distance_point_to_next()
        print(data)
        dx2 = data
        # Generación distribucion acumulada
        dx2.sort()
        out_threshold = 40.0
        net_dx2 = [i for i in dx2 if i < out_threshold]
        net_dx2 = np.array(net_dx2)
        net_dx2 = np.sort(net_dx2)
        cd_dx = np.linspace(0., 1., len(net_dx2))
        ser_dx = pd.Series(cd_dx, index=net_dx2)
        print(ser_dx)
        # plot
        plt.figure(figsize=(7, 8))
        plt.subplot(211)
        ser_dx.plot(drawstyle='default', legend="True")
        plt.xlabel("Meters")
        plt.ylabel("Frequency")
        plt.title("Cumulative distribution of distance point to point")
        plt.legend().set_visible(False)
        plt.grid(True)
        plt.subplot(212)
        plt.hist(net_dx2, bins=300, alpha=0.5)
        plt.xlabel('Distance point to point')
        plt.ylabel('Frequency')
        plt.title('Histogram of distance point to point')
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                            wspace=0.35)
        plt.show()
        # plt.savefig('distDist.eps', format='eps', dpi=600)
        self.assertEqual(True, True)

    def test_writting(self):
        mongodb_connection = MongoResourceImpl()
        track_information_repository = TrackStatisticsRepositoryImpl(mongodb_connection)
        id_track = "activity_3905397713"
        data = pd.DataFrame([[1, 2],
                             [3, 4],
                             [5, 6],
                             [7, 8],
                             [1, 2],
                             [1, 2]],
                            columns=['DistancePointProjection', 'DistanceToNext'])

        track_information_repository.write_track_statistics(id_track=id_track, data=data)
        print(data)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
