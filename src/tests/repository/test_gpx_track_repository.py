import unittest
from track_simulator.repository.resource.gpx_resource_impl import GPXResourceImpl as GPXTrackRepository
import matplotlib.pyplot as plt

class MyTestCase(unittest.TestCase):
    def test_gpx_file_Loading(self):
        test_file = GPXTrackRepository()
        parsed_file = test_file.read("tracks/Ficheros/RutasSegmentadas/RutaCastilloBellver1.gpx")
        self.assertEqual(len(parsed_file), 4)

    def test_gpx_file_Loading_2(self):
        test_file = GPXTrackRepository()
        parsed_file = test_file.read("../../rutaTramuntana.gpx")

        for p in parsed_file:
            plt.scatter(p.get_longitude(), p.get_latitude(), c="blue")
        plt.show()


if __name__ == '__main__':
    unittest.main()
