from track_analyzer.repository.graph_information_repository import GraphInformationRepository
from track_analyzer.repository.resource.mongo_resource import MongoResource
from track_analyzer.conf.config import MONGO_GRAPH_INFORMATION_COLLECTION
import pandas as pd


class GraphInformationRepositoryImpl(GraphInformationRepository):

    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def read_graph_information_dataframe(self, id_graph):
        query = {'graph_id': id_graph}
        print(id_graph, MONGO_GRAPH_INFORMATION_COLLECTION)
        data_from_db = self.mongo_resource.read(collection=MONGO_GRAPH_INFORMATION_COLLECTION,
                                                query=query)
        df = pd.DataFrame(data_from_db[0]["data"])
        return df

    def write_graph_information_dataframe(self, data):
        data_to_export = data[['source', 'target', 'num of detections', 'frequency']]
        today = pd.Timestamp('today')
        graph_id = 'Graph_Analysis_{:%m-%d-%Y}'.format(today)
        self.mongo_resource.write_graph(collection=MONGO_GRAPH_INFORMATION_COLLECTION,
                                        graph_id=graph_id,
                                        records=data_to_export.to_dict("records"))
