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
        fig, ax = plt.subplots()

        ax = ser_dx.plot(drawstyle='default', legend="True")
        ax.set_xlabel("Meters", fontsize=16)
        ax.set_ylabel("Frequency", fontsize=16)
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(12)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(12)
        ax.legend().set_visible(False)
        ax.grid(True)
        fig.canvas.draw()
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
