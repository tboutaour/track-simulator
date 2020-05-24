import os
import sys
import unittest
import importlib
from unittest import mock

j = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatordbbatch",
                                 "LAST_VERSION_GRAPH": "Graph_Analysis_05-02-2020",
                                 "MONGO_GRAPH_INFORMATION_COLLECTION": 'graphDataframe',
                                 "MONGO_TRACK_INFORMATION_COLLECTION": 'trackDataframe',
                                 'MONGO_TRACK_STATISTICS_COLLECTION': 'trackStatistics'}, clear=True)

k = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatordbempty",
                                 "LAST_VERSION_GRAPH": "Graph_Analysis_05-10-2020",
                                 "MONGO_GRAPH_INFORMATION_COLLECTION": 'graphDataframe',
                                 "MONGO_TRACK_INFORMATION_COLLECTION": 'trackDataframe',
                                 'MONGO_TRACK_STATISTICS_COLLECTION': 'trackStatistics'}, clear=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_read_point_to_next_superposed(self):
        with k:
            from track_simulator.repository.resource import mongo_resource_impl
            from track_simulator.repository import track_statistics_repository_impl
            mongodb_connection = mongo_resource_impl.MongoResourceImpl()
            track_information_repository = track_statistics_repository_impl.TrackStatisticsRepositoryImpl(
                mongodb_connection)
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

        with j:
            for i, v in sys.modules.items():
                if i.startswith('track_simulator.conf'):
                    print(i)
                    importlib.reload(v)
            for i, v in sys.modules.items():
                if i.startswith('track_simulator'):
                    print(i)
                    importlib.reload(v)
            from track_simulator.repository.resource import mongo_resource_impl
            from track_simulator.repository import track_statistics_repository_impl
            mongodb_connection = mongo_resource_impl.MongoResourceImpl()
            track_information_repository = track_statistics_repository_impl.TrackStatisticsRepositoryImpl(
                mongodb_connection)
            data2 = track_information_repository.read_distance_point_to_next()
            print(data2)
            dx22 = data2
            # Generación distribucion acumulada
            dx22.sort()
            out_threshold = 40.0
            net_dx22 = [i for i in dx22 if i < out_threshold]
            net_dx22 = np.array(net_dx22)
            net_dx22 = np.sort(net_dx22)
            cd_dx2 = np.linspace(0., 1., len(net_dx22))
            ser_dx2 = pd.Series(cd_dx2, index=net_dx22)
            print(ser_dx2)

        # plot
        plt.figure(figsize=(7, 8))
        plt.subplot(211)
        ser_dx.plot(drawstyle='default', legend="True", color='blue', label='Simulation')
        ser_dx2.plot(drawstyle='default', legend="True", color='red', label='Real')
        plt.xlabel("Meters")
        plt.ylabel("Frequency")
        plt.title("Cumulative distribution of distance point to point")
        plt.legend(loc="lower right", frameon=False)
        plt.grid(True)
        plt.subplot(212)
        plt.hist(net_dx22, bins=300, alpha=0.5, color='red', label='Real', normed=True)
        plt.hist(net_dx2, bins=300, alpha=0.5, color='blue', label='Simulation', normed=True)
        plt.xlabel('Distance point to point')
        plt.ylabel('Frequency')
        plt.title('Histogram of distance point to point')
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                            wspace=0.35)
        plt.legend(loc="upper right", frameon=False)
        plt.show()
        # plt.savefig('distDist.eps', format='eps', dpi=600)
        self.assertEqual(True, True)

    def test_writting(self):
        def test_read_point_projection(self):
            with k:
                from track_simulator.repository.resource import mongo_resource_impl
                from track_simulator.repository import track_statistics_repository_impl
                mongodb_connection = mongo_resource_impl.MongoResourceImpl()
                track_information_repository = track_statistics_repository_impl.TrackStatisticsRepositoryImpl(
                    mongodb_connection)
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
