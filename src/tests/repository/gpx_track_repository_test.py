import unittest

from src.track_analyzer.repository.gpx_track_repository_impl import GPXTrackRepositoryImpl as GPXTrackRepository


class MyTestCase(unittest.TestCase):
    def test_gpx_file_Loading(self):
        test_file = GPXTrackRepository("../../../tracks/Ficheros/RutasSegmentadas/RutaCastilloBellver1.gpx")
        parsed_file = test_file.parseFile()
        self.assertEqual(len(parsed_file), 4)

if __name__ == '__main__':
    unittest.main()
