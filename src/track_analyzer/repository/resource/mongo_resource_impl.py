from pymongo import MongoClient
from track_analyzer.conf.config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from track_analyzer.repository.resource.mongo_resource import MongoResource


def get_connection(host, port):
    return MongoClient(host, port)


class MongoResourceImpl(MongoResource):

    def read(self, collection, query):
        return get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].find(query)

    def write_graph(self, collection, graph_id, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert_one({"graph_id": graph_id,
                                                                                       "data": records})

    def write_statistics(self, collection, track_id, statistics_type, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert_one({"track_id": track_id,
                                                                                       "type": statistics_type,
                                                                                       "data": records})

    def write_many_statistics(self, collection, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert_many(records)

    def write_track(self, collection, track_id, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert_one({"track_id": track_id,
                                                                                       "data": records})

    def write_many_track(self, collection, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert_many(records)