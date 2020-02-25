from repository.graph_repository import GraphRepository
from pymongo import MongoClient
from networkx.readwrite import json_graph
import json


def get_connection(host, port):
    return MongoClient(host, port)


class GraphRepositoryImpl(GraphRepository):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = get_connection(host, port)

    def get_graph(self, id_graph):
        client = self.connection
        db = client.testdb
        collection = db.graph
        return json_graph.node_link_graph(collection.find({"id": id_graph}))

    def write_graph(self, graph):
        client = self.connection
        db = client.testdb
        collection = db.graph
        records = json_graph.node_link_data(graph)
        collection.insert(records)
