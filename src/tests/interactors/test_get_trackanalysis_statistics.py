import unittest
import pandas as pd
import numpy as np
from track_simulator.entities.track_point import TrackPoint as Point
from track_simulator.interactor.get_trackanalysis_statistics_impl import GetTrackAnalysisStatisticsImpl


class MyTestCase(unittest.TestCase):
    def test_path_creation(self):
        get_track_statistics = GetTrackAnalysisStatisticsImpl()
        id_track = 'activity_3276836874.gpx'

        input_data = pd.DataFrame([
            ['activity_3276836874.gpx', 2.623643483966589, 39.56738345324993,
            2.623551736100968, 39.56737690112559, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623629402369261, 39.56740231253207,
            2.6235503246574017, 39.567396665239926, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.6236156560480595, 39.56745771691203,
            2.6235463183093786, 39.567452765194815, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623613141477108, 39.56749141216278,
            2.6235439114319785, 39.567486468136444, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.6236106269061565, 39.56752711907029,
            2.623541361622155, 39.56752217252739, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623605765402317, 39.56754421815276,
            2.6235401220285683, 39.56753953026663, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623603083193302, 39.56756575964391,
            2.6235385778506086, 39.56756115302965, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.6235961262136698, 39.56758629530668,
            2.623537083448046, 39.56758207879942, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623588750138879, 39.567651925608516,
            2.623532382850435, 39.567647900169014, 1248507104, 317813195],
            ['activity_3276836874.gpx', 2.623586319386959, 39.56767112016678,
            2.6235310067028994, 39.567667170041275, 1248507104, 317813195]],
            columns=['id', 'Point_lat', 'Point_lon', 'Projection_lat', 'Projection_lon', 'Origin', 'Target'])
        expected_data = pd.DataFrame([
            [np.nan, 10.227825],
            [2.615371, 8.815387],
            [6.341207, 7.729599],
            [3.753243, 7.717594],
            [3.976109, 7.721522],
            [1.974767, 7.317761],
            [2.411310, 7.190896],
            [2.408672, 6.581941],
            [7.336100, 6.283686],
            [2.149164, 6.166121]],
            columns=['DistanceToNext', 'DistancePointProjection'])

        result = get_track_statistics.apply(input_data)

        pd.testing.assert_frame_equal(result, expected_data)
