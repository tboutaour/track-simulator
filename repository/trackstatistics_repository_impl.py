import json
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from repository.trackstatistics_repository import TrackStatisticsRepository


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
        collectionAcPointProjection = db.acPointProjection
        collectionAcBetweenPoints = db.acPointPoint
        pipeline = [
            {'$unwind': '$data'},
            {'$group': {'_id': None, 'data': {'$push': '$data'}}},
        ]
        distance_point_projection = list(collectionPointProjection.aggregate(pipeline, cursor={}))[0]
        distance_between_points = list(collectionPointPoint.aggregate(pipeline, cursor={}))[0]
        ac_dis_point_projection = list(collectionAcPointProjection.find().sort([("datetime", -1)]))[0]
        ac_dis_between_points = list(collectionAcBetweenPoints.find().sort([("datetime", -1)]))[0]

        return distance_point_projection, distance_between_points, ac_dis_point_projection, ac_dis_between_points

    def write_track_statistics(self,
                               id_track,
                               distance_point_projection,
                               ac_dis_point_projection,
                               distance_between_points,
                               ac_dis_between_points):
        client = self.connection
        db = client.testdb
        collectionPointProjection = db.distancePointProjection
        collectionPointPoint = db.distancePointPoint
        collectionAcPointProjection = db.acPointProjection
        collectionAcBetweenPoints = db.acPointPoint
        now = datetime.now()
        collectionPointProjection.insert({"datetime": now, "id_track": id_track, "data": distance_point_projection})
        collectionPointPoint.insert({"datetime": now, "id_track": id_track, "data": distance_between_points})
        collectionAcPointProjection.insert({"datetime": now, "id_track": id_track, "data": ac_dis_point_projection})
        collectionAcBetweenPoints.insert({"datetime": now, "id_track": id_track, "data": ac_dis_between_points})
