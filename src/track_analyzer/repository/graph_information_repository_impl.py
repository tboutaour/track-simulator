from src.track_analyzer.repository.graph_information_repository import GraphInformationRepository
from pymongo import MongoClient
import pandas as pd
import json


def get_connection(host, port):
    return MongoClient(host, port)


class GraphInformationRepositoryImpl(GraphInformationRepository):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = get_connection(host, port)

    def get_graphinformation_dataframe(self, id_graph):
        client = self.connection
        db = client.testdb
        collection = db.graphDataframe
        return pd.DataFrame(list(collection.find({"graph_id": id_graph})))

    def write_graphinformation_dataframe(self, data):
        client = self.connection
        db = client.testdb
        collection = db.graphDataframe
        data_to_export = data[['source', 'target', 'num of detections', 'frequency']]
        today = pd.Timestamp('today')
        data_to_export['graph_id'] = 'Graph_Analysis_{:%m%d%Y}'.format(today)
        print('Graph_Analysis_{:%m%d%Y}'.format(today))
        records = json.loads(data_to_export.T.to_json()).values()
        collection.insert(records)


