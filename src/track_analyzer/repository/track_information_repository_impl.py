from track_analyzer.repository.track_information_repository import TrackInformationRepository
from track_analyzer.repository.resource.mongo_resource import MongoResource
import pandas as pd
import json


class TrackInformationRepositoryImpl(TrackInformationRepository):

    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource


    def get_trackinformation_dataframe(self, id_track):
        query = {"id": id_track}
        self.mongo_resource.read(collection='trackdataframe', query=query)
        return pd.DataFrame(list(self.mongo_resource.read(collection='trackdataframe', query=query)))

    def write_trackinformation_dataframe(self, data):
        records = json.loads(data.T.to_json()).values()
        self.mongo_resource.write(collection='trackdataframe', records=records)
