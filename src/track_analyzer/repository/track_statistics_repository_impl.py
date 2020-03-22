from pymongo import MongoClient
from datetime import datetime
from src.track_analyzer.repository.track_statistics_repository import TrackStatisticsRepository


def get_connection(host, port):
    return MongoClient(host, port)


class TrackStatisticsRepositoryImpl(TrackStatisticsRepository):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = get_connection(host, port)

    def get_track_statistics(self):
        client = self.connection
        db = client.testdb
        collectionPointProjection = db.distancePointProjection
        collectionPointPoint = db.distancePointPoint
        pipeline = [
            {'$unwind': '$data'},
            {'$group': {'_id': None, 'data': {'$push': '$data'}}},
        ]
        distance_point_projection = list(collectionPointProjection.aggregate(pipeline, cursor={}))[0]
        distance_between_points = list(collectionPointPoint.aggregate(pipeline, cursor={}))[0]

        return distance_point_projection.get('data'), distance_between_points.get('data')

    def write_track_statistics(self,
                               id_track,
                               distance_point_projection,
                               distance_between_points):
        client = self.connection
        db = client.testdb
        collectionPointProjection = db.distancePointProjection
        collectionPointPoint = db.distancePointPoint
        now = datetime.now()
        collectionPointProjection.insert({"datetime": now, "id_track": id_track, "data": distance_point_projection})
        collectionPointPoint.insert({"datetime": now, "id_track": id_track, "data": distance_between_points})
