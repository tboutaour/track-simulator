from pymongo import MongoClient

from track_analyzer.repository.resource.mongo_resource import MongoResource
from track_analyzer.repository.track_statistics_repository import TrackStatisticsRepository


def get_connection(host, port):
    return MongoClient(host, port)


class TrackStatisticsRepositoryImpl(TrackStatisticsRepository):
    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def read_track_statistics(self):
        pass

    def write_track_statistics(self):
        pass