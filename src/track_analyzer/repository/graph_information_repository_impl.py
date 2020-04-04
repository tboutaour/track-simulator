from track_analyzer.repository.graph_information_repository import GraphInformationRepository
from track_analyzer.repository.resource.mongo_resource import MongoResource
import pandas as pd
import json


class GraphInformationRepositoryImpl(GraphInformationRepository):

    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def read_graph_information_dataframe(self, id_graph):
        query = {'graph_id': id_graph}
        return pd.DataFrame(list(self.mongo_resource.read(collection='graphDataframe', query=query)))

    def write_graph_information_dataframe(self, data):
        data_to_export = data[['source', 'target', 'num of detections', 'frequency']]
        today = pd.Timestamp('today')
        data_to_export['graph_id'] = 'Graph_Analysis_{:%m%d%Y}'.format(today)
        print('Graph_Analysis_{:%m%d%Y}'.format(today))
        records = json.loads(data_to_export.T.to_json()).values()
        self.mongo_resource.write(collection='graphDataframe', records=records)


