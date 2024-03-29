import unittest
from track_simulator.repository.track_information_repository_impl import TrackInformationRepositoryImpl
from track_simulator.repository.resource.mongo_resource_impl import MongoResourceImpl
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_reading(self):
        mongodb_connection = MongoResourceImpl()
        track_information_repository = TrackInformationRepositoryImpl(mongodb_connection)
        id_track = "activity_3905397717"
        data = track_information_repository.get_trackinformation_dataframe(id_track)
        print(data)
        self.assertEqual(True, True)

    def test_writting(self): #FIXME adapt test
        mongodb_connection = MongoResourceImpl()
        track_information_repository = TrackInformationRepositoryImpl(mongodb_connection)
        id_track = "activity_3905397717"
        data = pd.DataFrame([[1, 2, 1, 2, 1248507104, 317813195],
                             [3, 4, 1, 2, 1248507104, 317813195],
                             [5, 6, 1, 2, 1248507105, 317813195],
                             [7, 8, 1, 2, 1248507104, 317813195],
                             [1, 2, 1, 2, 1248507106, 317813195],
                             [1, 2, 1, 2, 1248507104, 317813195]],
                            columns=['Point_X', 'Point_Y', 'Projection_X', 'Projection_Y', 'Origin', 'Target'])

        track_information_repository.write_trackinformation_dataframe(id_track=id_track, data=data)
        print(data)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
