import unittest
from entities.GPXLoaderSaver_impl import GPXLoaderSaver as LoaderSaver
import gpxpy
import gpxpy.gpx


class MyTestCase(unittest.TestCase):
    def test_gpx_file_Loading(self):
        test_file = LoaderSaver("../tracks/Ficheros/RutasSegmentadas/RutaCastilloBellver1.gpx")
        parsed_file = test_file.parseFile()
        self.assertIsInstance(parsed_file, gpxpy.gpx.GPX)

if __name__ == '__main__':
    unittest.main()
