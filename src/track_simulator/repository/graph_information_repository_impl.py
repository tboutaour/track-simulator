from track_simulator.repository.graph_information_repository import GraphInformationRepository
from track_simulator.repository.resource.mongo_resource import MongoResource
from track_simulator.conf.config import MONGO_GRAPH_INFORMATION_COLLECTION
import pandas as pd


class GraphInformationRepositoryImpl(GraphInformationRepository):

    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def read_graph_information_dataframe(self, id_graph):
        query = {'graph_id': id_graph}
        print(id_graph, MONGO_GRAPH_INFORMATION_COLLECTION)
        data_from_db = self.mongo_resource.read(collection=MONGO_GRAPH_INFORMATION_COLLECTION,
                                                query=query)
        if data_from_db.count() < 1:
            any_data_from_db = self.mongo_resource.read(collection=MONGO_GRAPH_INFORMATION_COLLECTION,
                                                        query={})
            if any_data_from_db.count() > 0:
                return pd.DataFrame(any_data_from_db[0]["data"])
            else:
                raise Exception('There is no data in collection.')

        return pd.DataFrame(data_from_db[0]["data"])

    def write_graph_information_dataframe(self, data):
        data_to_export = data[['source', 'target', 'num of detections', 'frequency']]
        today = pd.Timestamp('today')
        graph_id = 'Graph_Analysis_{:%m-%d-%Y}'.format(today)
        self.mongo_resource.write_graph(collection=MONGO_GRAPH_INFORMATION_COLLECTION,
                                        graph_id=graph_id,
                                        records=data_to_export.to_dict("records"))
