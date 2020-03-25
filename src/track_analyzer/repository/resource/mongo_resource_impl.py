from pymongo import MongoClient
from src.track_analyzer.conf.config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from src.track_analyzer.repository.resource.mongo_resource import MongoResource

def get_connection(host, port):
    return MongoClient(host, port)


class MongoResourceImpl(MongoResource):

    def read(self, collection, query):
        return get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].find(query)

    def write(self, collection, records):
        get_connection(MONGO_HOST, MONGO_PORT)[MONGO_DATABASE][collection].insert(records)
