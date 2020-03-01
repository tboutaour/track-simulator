from repository.Trackinformation_repository import TrackInformationRepository
from pymongo import MongoClient
import pandas as pd
import json


def get_connection(host, port):
    return MongoClient(host, port)


class TrackInformationRepositoryImpl(TrackInformationRepository):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = get_connection(host, port)

    def get_trackinformation_dataframe(self, id_track):
        client = self.connection
        db = client.testdb
        collection = db.trackdataframe
        return pd.DataFrame(list(collection.find({"id": id_track})))

    def write_trackinformation_dataframe(self, data):
        client = self.connection
        db = client.testdb
        collection = db.trackdataframe
        records = json.loads(data.T.to_json()).values()
        collection.insert(records)
