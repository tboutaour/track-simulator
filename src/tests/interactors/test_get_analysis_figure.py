import os
import unittest
from unittest import mock

k = mock.patch.dict(os.environ, {"MONGO_HOST": "localhost",
                                 "MONGO_PORT": "27019",
                                 "MONGO_DATABASE": "tracksimulatordbbatch",
                                 "LAST_VERSION_GRAPH": "Graph_Analysis_05-10-2020",
                                 'MONGO_TRACK_STATISTICS_COLLECTION': 'trackStatistics',
                                 "EXPORT_ANALYSIS_IMAGES_FOLDER": "/Users/tonibous/Documents/1-UIB/TrabajoFinal"
                                                                  "/TrackAnalyzer/src/data/analysis/statistics"}, clear=True)


class MyTestCase(unittest.TestCase):
    def test_analysis_figure_projection(self):
        with k:
            from track_analyzer.interactor import get_analysis_figure_impl
            from track_analyzer.repository.resource import mongo_resource_impl
            from track_analyzer.repository import track_statistics_repository_impl
            mongodb_connection = mongo_resource_impl.MongoResourceImpl()
            track_information_repository = track_statistics_repository_impl.TrackStatisticsRepositoryImpl(
                mongodb_connection)
            data = track_information_repository.read_distance_point_projection()
            get_analysis_figure = get_analysis_figure_impl.GetAnalysisFigureImpl()
            get_analysis_figure.apply_distance_point_projection(data)

    def test_analysis_figure_point(self):
        with k:
            from track_analyzer.interactor import get_analysis_figure_impl
            from track_analyzer.repository.resource import mongo_resource_impl
            from track_analyzer.repository import track_statistics_repository_impl
            mongodb_connection = mongo_resource_impl.MongoResourceImpl()
            track_information_repository = track_statistics_repository_impl.TrackStatisticsRepositoryImpl(
                mongodb_connection)
            data = track_information_repository.read_distance_point_to_next()
            get_analysis_figure = get_analysis_figure_impl.GetAnalysisFigureImpl()
            get_analysis_figure.apply_distance_point_point(data)
