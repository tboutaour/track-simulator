from track_simulator.interactor.get_trackanalysis_statistics import GetTrackAnalysisStatistics
from track_simulator.entities.track_point import TrackPoint as Point
import pandas as pd
from pandas import DataFrame


class GetTrackAnalysisStatisticsImpl(GetTrackAnalysisStatistics):
    def apply(self, data: DataFrame) -> DataFrame:
        data = self.__add_point_projection_distance(data)
        data = self.__add_next_point_distance(data)
        return data[['id', 'DistanceToNext', 'DistancePointProjection']]

    def __add_next_point_distance(self, data: DataFrame) -> DataFrame:
        data['point_lon_shift'] = data.Point_lon.shift()
        data['point_lat_shift'] = data.Point_lat.shift()
        data['DistanceToNext'] = data.apply(lambda x: Point(x['Point_lon'], x['Point_lat']).haversine_distance(
            Point(x['point_lon_shift'],
                  x['point_lat_shift'])),
                                            axis=1)
        return data.drop(columns=['point_lat_shift', 'point_lon_shift'])

    def __add_point_projection_distance(self, data: DataFrame) -> DataFrame:
        data['DistancePointProjection'] = data.apply(lambda x: Point(x['Point_lon'],
                                                                     x['Point_lat']).haversine_distance(
            Point(x['Projection_lon'],
                  x['Projection_lat'])),
                                                     axis=1)
        return data

