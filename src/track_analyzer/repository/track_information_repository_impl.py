from track_analyzer.repository.track_information_repository import TrackInformationRepository
from track_analyzer.repository.resource.mongo_resource import MongoResource
from track_analyzer.conf.config import MONGO_TRACK_INFORMATION_COLLECTION
import pandas as pd


class TrackInformationRepositoryImpl(TrackInformationRepository):

    def __init__(self, mongo_resource: MongoResource):
        self.mongo_resource = mongo_resource

    def get_trackinformation_dataframe(self, id_track):
        query = {'track_id': id_track}
        data_from_db = self.mongo_resource.read(collection=MONGO_TRACK_INFORMATION_COLLECTION, query=query)
        df = pd.DataFrame(data_from_db[0]["data"])
        return df

    def write_trackinformation_dataframe(self, id_track, data):
        self.mongo_resource.write_track(collection=MONGO_TRACK_INFORMATION_COLLECTION,
                                        track_id=id_track,
                                        records=data.to_dict("records"))

    def write_trackinformation_dataframes(self, data):
        records = [{'track_id': d['id'][0], 'data': d.to_dict("records")} for d in data]
        self.mongo_resource.write_many_track(collection=MONGO_TRACK_INFORMATION_COLLECTION, records=records)
