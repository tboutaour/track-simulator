from pymongo import MongoClient
from pandas import DataFrame
from track_simulator.repository.resource.mongo_resource import MongoResource
from track_simulator.repository.track_statistics_repository import TrackStatisticsRepository
from track_simulator.conf.config import MONGO_TRACK_STATISTICS_COLLECTION

POINT_PROJECTION = 'point-projection'
POINT_TO_NEXT = 'point-to-next'


def get_connection(host, port):
    return MongoClient(host, port)


class TrackStatisticsRepositoryImpl(TrackStatisticsRepository):
    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def read_distance_point_projection(self):
        query = {'type': POINT_PROJECTION}
        data_from_db = self.mongo_resource.read(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                                query=query)
        return sum([a['data'] for a in data_from_db], [])

    def read_distance_point_to_next(self):
        query = {'type': POINT_TO_NEXT}
        data_from_db = self.mongo_resource.read(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                                query=query)
        return sum([a['data'] for a in data_from_db], [])

    def write_track_statistics(self, id_track, data: DataFrame):
        # Write list of distance Point-Projection
        distance_point_projection = data['DistancePointProjection'].tolist()
        # Write list of distance to next point
        distance_point_to_next = data['DistanceToNext'].tolist()
        # Insert 1 in mongoDB
        self.mongo_resource.write_statistics(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                             track_id=id_track,
                                             statistics_type='point-projection',
                                             records=distance_point_projection)
        # Insert 2 in mongoDB
        self.mongo_resource.write_statistics(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                             track_id=id_track,
                                             statistics_type='point-to-next',
                                             records=distance_point_to_next)

    def write_many_track_statistics(self, data: DataFrame):
        # Write list of distance Point-Projection
        point_projection_data = [{'track_id': d['id'][0],
                                  'type': 'point-projection',
                                  'data': d['DistancePointProjection'].tolist()} for d in data]

        # Write list of distance to next point
        point_to_next_data = [{'track_id': d['id'][0],
                               'type': 'point-to-next',
                               'data': d['DistanceToNext'].tolist()}
                              for d in data]

        # Insert 1 in mongoDB
        self.mongo_resource.write_many_statistics(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                                  records=point_projection_data)
        # Insert 2 in mongoDB
        self.mongo_resource.write_many_statistics(collection=MONGO_TRACK_STATISTICS_COLLECTION,
                                                  records=point_to_next_data)
