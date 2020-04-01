import unittest
from src.track_analyzer.entities.track_point import TrackPoint
from src.track_analyzer.entities.track_segment import TrackSegment as Segment

class MyTestCase(unittest.TestCase):
    def test_segment_operations(self):
        point = TrackPoint(2, 1)
        point_b = TrackPoint(4, 4)
        segm = Segment([point.get_longlat(), point_b.get_longlat()])

        self.assertEqual(point.get_longitude(), 2)
        self.assertEqual(point.haversine_distance(point_b), 400787.4747541121)
        self.assertEqual(segm.get_points(), [(2, 1), (4, 4)])
        self.assertEqual(segm.get_distance(), 400787.4747541121)
        segm = segm.add_point(point.get_longlat())
        segm = segm.add_point(point.get_longlat())
        self.assertEqual(segm.get_points(), [(2.0, 1.0), (4.0, 4.0), (2.0, 1.0), (2.0, 1.0)])
        self.assertEqual(point.get_bearing(point_b), 33.62695665710845)

    def test_point_operations(self):
        point = TrackPoint(2, 1)
        point_b = TrackPoint(4,4)
        self.assertEqual(point.get_latitude(), 1)
        self.assertEqual(point.get_longitude(), 2)
        self.assertEqual(point.haversine_distance(point_b), 400787.4747541121)


if __name__ == '__main__':
    unittest.main()

